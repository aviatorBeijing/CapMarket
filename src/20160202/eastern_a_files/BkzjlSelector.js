var Class={create:function(){return function(){this.initialize.apply(this,arguments)}}};Object.extend=function(a,b){for(property in b){a[property]=b[property]}return a};var BkzjlxPop=Class.create();Object.extend(BkzjlxPop.prototype,{initialize:function(a){var b=this;Object.extend(b.options,a||{});b.popDiv()},options:{obj:"selector",objClose:"close",objPop:"pop"},popDiv:function(){var g=this;var a=document.getElementById(g.options.obj);var h=document.getElementById(g.options.objClose);var j=document.getElementById(g.options.objPop);var k=j.getElementsByTagName("a");var g=this;var e=function(){j.style.display="none"};var c=function(){j.style.display=""};var b=function(l,i){if(i=="over"){if(!g.tools.hasClass(l,"hover")){g.tools.addClass(l,"hover")}}else{g.tools.removeClass(l,"hover")}};g.tools.addEvent(a,"click",c);g.tools.addEvent(h,"click",e);for(var d=0,f=k.length;d<f;d++){g.tools.addEvent(k[d],"mouseover",b.bind(this,k[d],"over"));g.tools.addEvent(k[d],"mouseout",b.bind(this,k[d],"out"));g.tools.addEvent(k[d],"click",e)}},tools:{addEvent:function(e,b,c,a){if(e.addEventListener){e.addEventListener(b,c,a);return true}else{if(e.attachEvent){var d=e.attachEvent("on"+b,c);return d}else{e["on"+b]=c}}},getArrayOfClassNames:function(a){var b=[];if(a.className){b=a.className.split(" ")}return b},addClass:function(a,b){var c=this.getArrayOfClassNames(a);c.push(b);a.className=c.join(" ")},removeClass:function(b,c){var e=this.getArrayOfClassNames(b);var d=[];for(var a=0;a<e.length;a++){if(c!=e[a]){d.push(e[a])}}if(d.length==0){b.className=null}else{b.className=d.join(" ")}},hasClass:function(c,d){var b=false;var e=this.getArrayOfClassNames(c);for(var a=0;a<e.length;a++){if(d==e[a]){b=true}}return b}}});Function.prototype.bind=function(){var d=this,b=arguments[0],a=new Array();for(var c=1;c<arguments.length;c++){a.push(arguments[c])}return function(){return d.apply(b,a)}};
// 2012-04-23 13:28:57.45  