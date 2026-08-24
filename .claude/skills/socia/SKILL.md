---
name: socia
description: "Manual do Agente 15 (Sósia) — como montar um painel de referência anti-drift e configurar personagens/produtos/estilos fixos na Biblioteca do Magnific, e como ensinar esse método pro usuário. Use quando for organizar a consistência visual de um personagem/produto entre várias gerações de imagem, ou quando o usuário perguntar como reduzir drift / configurar modelos no Magnific."
---

# Sósia — manual de consistência visual (painel de referência + Biblioteca do Magnific)

## O problema que isso resolve (explique assim, sem jargão)

Toda vez que se gera uma imagem nova de um personagem a partir só de **texto**, ou a partir de uma imagem antiga escolhida "no olho", uma parte da identidade visual se perde um pouco — a orelha fica mais fina, a pata desaparece, o traço afina. Isso é o **drift**: o personagem "derrapando" pra uma versão sutilmente diferente a cada geração nova, até que, depois de várias rodadas, ele não é mais o mesmo bicho.

A cura pra isso tem duas partes, e as duas importam:

1. **Um painel de referência completo** — um lugar único, visual, com todas as vistas e expressões já aprovadas do personagem (não uma imagem solta).
2. **Um jeito de apontar pra esse painel de forma barata e repetível** — sem precisar caçar manualmente qual imagem antiga usar a cada nova cena.

No Magnific, a parte 2 chama **Biblioteca** (`library_create`): você registra o personagem UMA vez, e da em diante toda geração nova aponta pro nome/id dele, em vez de escolher uma criação antiga.

## Passo 1 — Achar (não inventar) a base de verdade

Antes de montar qualquer painel, procure o que já existe:
- Um documento de contrato/guia já travado do personagem (busque por nomes como `*CONTRATO*.md`, `*DESIGN_SYSTEM*.md`, `*PERSONA*.md` na raiz do repo do produto).
- Memória do hub (`memoria/` ou o sistema de memória do Claude) — pode já existir registro de decisões de anatomia/cor/traço tomadas em sessões anteriores.
- Uma ilustração-base já aprovada, mesmo que solta (pasta de referências do projeto).

Se existir contrato: ele é a fonte da verdade, ponto final — não reabra debate de anatomia/cor/traço já fechado ali, mesmo que um resultado pareça "podia ser melhor assim". Se não existir nada: primeiro proponha a direção de estilo (pesquise Mobbin se fizer sentido) e confirme com o usuário antes de gerar em lote.

## Passo 2 — O que é um painel de referência "completo"

Um bom painel de referência tem, no mínimo:

- **Turnaround/model sheet** de cada personagem: pelo menos 3 ângulos (frente, ¾, perfil), idealmente 6-8 (+ trás, ¾-trás, topo, trás-direto).
- **Expression sheet**: as expressões que o personagem realmente vai precisar no produto (feliz, triste, surpreso, preocupado, etc. — não genérico, e sim o que o produto de fato usa).
- **Poses-chave já aprovadas**: as interações/cenas que já passaram por rodadas de correção e foram aceitas (ex.: abraço, sentado, cumprimento). Cada pose aprovada é uma referência valiosa — não descartar depois de usada uma vez.

**Onde montar:** Figma é preferível a uma pasta de imagens soltas — é visual, versionável, compartilhável com o time, e dá pra anotar ao lado de cada painel qual regra não pode variar. Um exemplo real desse tipo de painel (turnaround + expressões de 2 personagens + poses + vinhetas de uso, tudo numa prancheta só) é o que motivou este agente a existir — ver a memória do projeto que documentar esse caso (tipo `reference`, se existir) para o link exato.

**Achado útil:** ao inspecionar uma prancheta de Figma que já foi montada colando resultados do Magnific, cheque a metadata (`get_metadata`) por camadas ocultas nomeadas `magnific_<algo>_<identifier>` — o identifier real da criação-fonte às vezes fica incrustado no nome da camada. Isso permite recuperar a criação original sem precisar adivinhar via `creations_search`.

## Passo 3 — Subir arquivo local pro Magnific sem fricção

Quando você já tem o arquivo em disco (ex.: um model sheet salvo no repo do projeto), não peça pro usuário fazer upload manual pelo widget — isso só é necessário quando o arquivo NÃO existe localmente (ex.: algo que o usuário colou direto no chat, sem salvar em disco). Pra arquivo local, o fluxo é 3 chamadas, sem interação nenhuma:

```
1. mcp__magnific__creations_request_upload  → { mimeType: "image/png" }
   (retorna proxyUploadUrl + path)

2. Bash:
   curl -sS -X PUT -H "Content-Type: image/png" \
     --data-binary @"/caminho/do/arquivo.png" \
     "<proxyUploadUrl>"

3. mcp__magnific__creations_finalize_upload → { path: "<path retornado no passo 1>" }
   (retorna { identifier: "<10 caracteres>" })
```

Esse `identifier` de 10 caracteres é o que vale para `references: [{type: "image", identifier: "..."}]` numa geração — **mas não é o mesmo tipo de id que a Biblioteca usa** (ver Passo 4). Pra subir várias imagens de uma vez, `creations_request_upload` aceita `count`, e `creations_finalize_upload` aceita `uploads: [{path}, ...]`.

Se o arquivo só existe como URL pública (não local), pule os 3 passos e use `creations_upload_image({url})` direto.

## Passo 4 — Registrar como asset fixo na Biblioteca

```
mcp__magnific__library_create({
  name: "projeto-personagem-descricao",   // único, kebab-case, só letras/dígitos/_/-
  type: "character",                       // ou "style" | "product" | "locations"
  images: [{ creationIdentifier: "<identifier do passo 3>" }],  // 1-6 imagens; a 1ª é a capa
  description: "..."                       // as regras de anatomia/traço/cor que NÃO podem variar
})
```

Retorna `{ id: <número>, identifier: "<10 caracteres>", webUrl: ... }`. **Ponto de atenção que já causou confusão:** ao usar esse asset numa geração futura, o `identifier` do `references[]` pro tipo `character`/`product`/`locations`/`style`-LoRA é o **`id` numérico**, não a string de 10 caracteres (essa string de 10 caracteres é só pro tipo `image`, que aponta pra uma criação avulsa, não pra um asset de biblioteca):

```
references: [{ type: "character", identifier: "2152881" }]   // id numérico, como string
```

`library_create` **não treina LoRA** — é registro de imagens de referência, não geração de modelo. Por isso é rápido e não tem custo perceptível. Um personagem pode (e deve) ter seu asset atualizado depois com `library_edit` se o design oficial mudar.

**Quando usar `character` vs `image` como reference:** um asset de `character` bem montado (várias vistas/expressões numa imagem-fonte de qualidade) costuma dar mais controle de identidade do que apontar pra uma criação de casal/cena antiga — mas ainda vale testar os dois lados a lado num projeto novo, porque em cenas com MAIS DE UM personagem interagindo (ex.: um casal se abraçando), uma imagem de referência que já mostra os dois juntos interagindo corretamente pode carregar informação de composição que dois `character` isolados não carregam. Registre o que funcionou melhor na memória do projeto pra próxima sessão não teste do zero de novo.

## Passo 5 — Validar antes de generalizar

Depois de criar o asset, gere 1-2 cenas de teste usando-o e **dê zoom** nos pontos que esse projeto já sabe que costumam falhar (checklist específico do projeto — ex.: contagem de patas, espessura de traço, espelhamento entre duas figuras). Só declare o setup "pronto pra uso" depois dessa checagem visual — nunca assuma que "a Biblioteca resolve tudo" sem checar o resultado real.

## Passo 6 — Documentar (senão o trabalho se perde)

Sem isso, cada sessão nova recomeça a busca do zero. Salve na memória do projeto (tipo `reference`) pelo menos:
- Onde fica o painel de referência mestre (link/caminho).
- Os `id`s/`identifier`s de cada asset de Biblioteca criado e pra que personagem/produto cada um serve.
- Qualquer regra de anatomia/traço/cor que já foi fechada e não deve ser reaberta (linkar pra memória de feedback correspondente, se existir).

## Passo 7 — Ensinar (isso é entrega, não bônus)

Feche sempre explicando pro usuário, em linguagem de designer:

> "Um painel de referência é como a 'carteira de identidade visual' do personagem: todas as vistas e expressões que ele pode ter, num só lugar. Toda vez que a IA desenha uma cena nova, ela erra menos quando aponta pra essa carteira em vez de tentar 'lembrar de cabeça' — isso é reduzir o drift. O Magnific tem um jeito de fixar essa carteira: você registra o personagem uma vez (a Biblioteca), e da em diante só aponta pro nome dele em vez de escolher uma imagem antiga a cada vez."

E entregue um roteiro replicável curto (adapte aos passos 1-6 acima) pra que o usuário — ou uma sessão futura, com outro personagem, em outro projeto — consiga repetir sozinho:
1. Ache/organize o painel de referência completo do personagem (turnaround + expressões + poses aprovadas).
2. Suba as peças-chave pro Magnific (upload local, sem fricção).
3. Registre como asset de Biblioteca (`library_create`), guardando o `id` numérico.
4. Gere 1-2 cenas de teste e confira de perto antes de confiar no setup.
5. Documente o `id` e o link do painel na memória do projeto.
