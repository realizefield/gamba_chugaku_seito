const katex=require('katex');const rl=require('readline').createInterface({input:process.stdin});
rl.on('line',l=>{const t=JSON.parse(l);let out;try{out=katex.renderToString(t,{throwOnError:true,output:'html',displayMode:false,strict:false});}catch(e){out=null}
process.stdout.write(JSON.stringify(out)+"\n");});
