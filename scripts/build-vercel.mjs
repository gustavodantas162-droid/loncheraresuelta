import fs from 'node:fs/promises';
import ts from 'typescript';
const out = 'out';
await fs.mkdir(out, {recursive:true});
await fs.cp('public',out,{recursive:true});
const content=await fs.readFile('app/content.ts','utf8');
const html=JSON.parse(content.split(' = ')[1].trim().replace(/;$/,''));
const css=await fs.readFile('app/globals.css','utf8');
const layout=await fs.readFile('app/layout.tsx','utf8');
const fonts=layout.match(/href="(https:\/\/fonts.googleapis.com\/css2[^\"]+)"/)[1];
await fs.writeFile(`${out}/styles.css`,css);
const source=await fs.readFile('app/interactions.ts','utf8');
const js=ts.transpileModule(source,{compilerOptions:{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.ES2022}}).outputText;
await fs.writeFile(`${out}/interactions.js`,js+'\ninitializePage(document.body);\n');
await fs.writeFile(`${out}/index.html`,`<!doctype html>
<html lang="es-419"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Lonchera Resuelta</title><meta name="description" content="Cuatro semanas de loncheras organizadas en un solo PDF. 20 combinaciones, 40 recetas y 4 listas de compras.">
<meta property="og:title" content="Lonchera Resuelta"><meta property="og:description" content="Mañana hay clases. La lonchera ya tiene plan."><meta property="og:image" content="https://loncheraresuelta.vercel.app/images/lonchera-16.webp"><meta property="og:type" content="website">
<link rel="icon" href="/favicon.svg"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="${fonts.replaceAll('&','&amp;')}"><link rel="stylesheet" href="/styles.css">
<script src="/tracking.js"></script></head>
<body><main style="font-weight:600">${html}</main><script type="module" src="/interactions.js"></script></body></html>`);
await fs.writeFile(`${out}/vercel.json`,JSON.stringify({version:2,cleanUrls:true}));
console.log('Vercel static build ready in out/.');

