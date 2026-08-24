# Figma snippets (use_figma) — code→figma

Sempre carregue a skill `figma-use` antes de `use_figma`. Código roda em contexto async; use `return` para devolver dados; cores em 0–1; **retorne os IDs** criados/alterados.

## Resolver token (alias → hex concreto, modo Light)
```js
const cols = await figma.variables.getLocalVariableCollectionsAsync();
async function resolve(varName){
  const all = await figma.variables.getLocalVariablesAsync('COLOR');
  let v = all.find(x => x.name === varName);
  if(!v) return {name:varName, err:'not found'};
  let col = cols.find(c => c.id === v.variableCollectionId);
  let modeId = col.modes.find(m => m.name==='Light')?.modeId || col.modes[0].modeId;
  for(let i=0;i<10;i++){
    let val = v.valuesByMode[modeId];
    if(val && val.type === 'VARIABLE_ALIAS'){
      v = await figma.variables.getVariableByIdAsync(val.id);
      col = cols.find(c => c.id === v.variableCollectionId);
      modeId = col.modes.find(m => m.name==='Light')?.modeId || col.modes[0].modeId;
      continue;
    }
    const f = x => Math.round(x*255).toString(16).padStart(2,'0');
    return {name:varName, hex:'#'+f(val.r)+f(val.g)+f(val.b), prim:v.name};
  }
}
```

## Vincular variável a um fill/stroke (boundSolid)
```js
const colorVars = await figma.variables.getLocalVariablesAsync('COLOR');
const V = n => colorVars.find(v => v.name === n);
function boundSolid(varName, base){
  let p = {type:'SOLID', color: base || {r:0.5,g:0.5,b:0.5}};
  return figma.variables.setBoundVariableForPaint(p, 'color', V(varName));
}
// node.fills = [ boundSolid('Background/Background Primary') ];
// node.strokes = [ boundSolid('Border/Border Primary') ]; node.strokeWeight = 1;
```

## Container auto-layout + texto (recipe)
```js
await figma.loadFontAsync({family:'Satoshi', style:'Bold'});
await figma.loadFontAsync({family:'Satoshi', style:'Medium'});

const card = figma.createAutoLayout('VERTICAL', { name:'Card', itemSpacing:16 });
card.paddingTop = card.paddingBottom = card.paddingLeft = card.paddingRight = 24;
card.cornerRadius = 12;
card.resize(360, 100);                 // resize ANTES dos modos
card.counterAxisSizingMode = 'FIXED';  // largura fixa (layout vertical)
card.primaryAxisSizingMode = 'AUTO';   // altura hug
card.fills = []; // <- frames de grupo SEM fundo: limpe o branco padrão

const t = figma.createText();
t.fontName = {family:'Satoshi', style:'Bold'}; t.fontSize = 16;
t.lineHeight = {unit:'PIXELS', value:24};
t.characters = '...';
card.appendChild(t); t.layoutSizingHorizontal = 'FILL'; // só após append
t.textAutoResize = 'HEIGHT';
```

## Reuse de ícone oficial + recolor correto
```js
const comp = await figma.importComponentByKeyAsync('<componentKey>'); // de search_design_system
const icon = comp.createInstance(); card.appendChild(icon); icon.resize(28,28);
// limpe fill do container interno (senão vira quadrado), recolora só os glifos com stroke:
const inner = icon.findOne(n => n.type==='INSTANCE');
if (inner) inner.fills = [];
for (const g of icon.findAll(n => n.type==='VECTOR' && Array.isArray(n.strokes) && n.strokes.length)){
  g.strokes = [ boundSolid('Content/Content Brand') ];
}
```

## Component set de estados (variantes)
```js
const enable = figma.createComponentFromNode(card); enable.name = 'Propriedades=Enable';
const comps = [enable];
for (const [state,cfg] of Object.entries(STATES)){
  const c = enable.clone(); c.name = 'Propriedades='+state; restyle(c,cfg); comps.push(c);
}
const set = figma.combineAsVariants(comps, parentFrame);
set.name = 'Card - ...';
set.layoutMode='HORIZONTAL'; set.layoutWrap='WRAP';
set.itemSpacing=32; set.counterAxisSpacing=32;
set.paddingTop=set.paddingBottom=set.paddingLeft=set.paddingRight=40;
set.resize(1224, set.height);
set.primaryAxisSizingMode='FIXED';   // largura fixa força o wrap
set.counterAxisSizingMode='AUTO';    // altura hug
for (const c of set.children){ c.counterAxisSizingMode='FIXED'; c.primaryAxisSizingMode='AUTO'; }
return { setId:set.id, variants: comps.map(c=>({name:c.name,id:c.id})) };
```

## Efeitos (box-shadow → DROP_SHADOW)
```js
const SHADOW = { type:'DROP_SHADOW', color:{r:0,g:0,b:0,a:0.10}, offset:{x:0,y:4}, radius:10, spread:0, visible:true, blendMode:'NORMAL' };
const FOCUS_GLOW = { type:'DROP_SHADOW', color:{r:0.42,g:0.33,b:0.85,a:0.25}, offset:{x:0,y:0}, radius:0, spread:4, visible:true, blendMode:'NORMAL' };
// node.effects = [SHADOW];  // anel de foco: também strokes=[boundSolid('Border/Border Focus')], strokeWeight=2, strokeAlign='OUTSIDE'
```

## Imagens/logos reais — MÉTODO CONFIÁVEL: `upload_assets` + curl
No `use_figma`: `fetch`/`XMLHttpRequest` NÃO existem e `createImageAsync(url)` lança "not a supported API". Transcrever base64 grande à mão corrompe. **A forma certa de embutir o PNG REAL é o tool oficial `mcp__claude_ai_Figma__upload_assets`** (sobe os bytes do arquivo via curl — zero transcrição):

1. No `use_figma`, crie um RECT do tamanho de exibição no lugar do asset e retorne o id:
   ```js
   const r = figma.createRectangle(); r.name='logo-primary'; r.resize(115,18); r.fills=[];
   logoFrame.appendChild(r); return { rect: r.id };
   ```
2. Chame `upload_assets({ fileKey, nodeId: <rectId>, count:1, scaleMode:'FIT' })` → retorna um `submitUrl` de uso único.
3. POSTe o arquivo real (multipart preferido) — o asset vira fill do nó:
   ```bash
   curl -s -X POST -F "file=@<PRODUTO>/webclient/public/img/logo-primary.png;type=image/png" \
     "<submitUrl>"   # resposta: { success:true, imageHash, placedOnNodeId }
   ```
   (`scaleMode` FIT preserva proporção do wordmark; FILL para ícone quadrado.)

Suporta PNG/JPG/GIF/WebP (máx 10MB). **SVG não** — para SVG use `figma.createNodeFromSvg()` no `use_figma`.

Fallback (sem MCP de upload): só asset minúsculo via `figma.createImage(figma.base64Decode(B64))`, conferindo o render. Stand-in colorido é último recurso e **sempre com a cor real do asset** (nunca inventada).

## Container → instâncias do sub-componente (refactor)
Cada item do container deve ser uma INSTÂNCIA do sub-componente (assim carrega os estados).
```js
const inst = variantComp.createInstance();          // variante certa (ex.: State=Active)
menus.appendChild(inst); inst.layoutSizingHorizontal='FILL';
// trocar o ícone nested + RECOLOR depois do swap (swap traz a cor original):
const iconInst = inst.findOne(n => n.type==='INSTANCE');
iconInst.swapComponent(await figma.importComponentByKeyAsync(KEY));
iconInst.resize(20,20); recolor(iconInst, LIGHT_OR_WHITE);
// override de texto e de elementos opcionais:
const lbl = inst.findOne(n => n.type==='TEXT' && n.characters!=='NOVO'); lbl.characters = label;
const tag = inst.findOne(n => n.name==='tag'); tag.visible = !!hasTag;  // inclua a tag no componente, oculta por padrão
```

## Variantes multi-eixo (Layout × State) no MESMO set
```js
// renomeie as existentes e ANEXE novas ao set — o set passa a expor as 2 props
existing.name = 'Layout=Expanded, State=Default';
const c = figma.createComponentFromNode(rowCollapsed);
c.name = 'Layout=Collapsed, State=Default';
set.appendChild(c);                  // adiciona como variante (nomes definem as props)
// set.componentPropertyDefinitions agora tem { Layout, State }
```

## Screenshot inline para validar
```js
return await card.screenshot(); // ou get_screenshot(nodeId) separado
```
