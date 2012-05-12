function vnc_console(win){
    var nw = window.open(win, 
                         "_blank", "innerWidth=640,innerheight=400","titlebar=no,toolbar=no,scrollbars=no,resizable=no");
    nw.focus();
}

function wresize() {
   var ps;
   try { 
     ps = document.vncapp.getPreferredSize();
   } catch (e) {
     setTimeout ("wresize()", 100);
     return;
   }

   var aw = ps.width;
   var ah = ps.height;
   var oh;
   var ow;

   if (!window.innerHeight && document.body && document.body.offsetHeight) {
     // hack for IE
     oh = document.documentElement.clientHeight;
     ow = document.documentElement.clientWidth;
   }  else {
     // other browsers
     oh = window.innerHeight;
     ow = window.innerWidth;
   }

   document.vncapp.style.height = ah + "px";
   document.vncapp.style.width = aw + "px";

   var offsetw = aw - ow + 4;
   var offseth = ah - oh + 4;

   if (offsetw !== 0 || offseth !== 0) {
     try { window.resizeBy(offsetw, offseth); } catch (e) {}
   }

   setTimeout ("wresize()", 1000);
 }
