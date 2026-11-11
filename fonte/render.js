const {chromium}=require('playwright');
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage();
 await p.goto('file://'+process.cwd()+'/devocional.html',{waitUntil:'load'});
 await p.evaluate(()=>document.fonts.ready);
 await p.pdf({path:process.argv[2]||'devocional.pdf',preferCSSPageSize:true,printBackground:true,outline:true,tagged:true});
 await b.close();
})();
