import {initWasm,Resvg} from '@resvg/resvg-wasm';
import wasm from '@resvg/resvg-wasm/index_bg.wasm';
import oswald from './assets/Oswald.bin';
import serif from './assets/LiberationSerif.bin';
import template from './assets/ticket.svg';
import {ticketSVG} from './ticket.mjs';
let ready;
export async function renderTicket(position,user) {
 ready ??= initWasm(wasm); await ready;
 const renderer=new Resvg(ticketSVG(template,position,user),{font:{fontBuffers:[new Uint8Array(oswald),new Uint8Array(serif)],loadSystemFonts:false}});
 let image;
 try {image=renderer.render(); return image.asPng();} finally {image?.free();renderer.free();}
}
