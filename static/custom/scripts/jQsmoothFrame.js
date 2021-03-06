var smoothFrame = {
    shortcuts : {
        sF: function() { return smoothFrame; },
        sFo: function() { with(smoothFrame.shortcuts){ return sF().options; } },
        sFosE: function() { with(smoothFrame.shortcuts){ return sFo().sourceElement; } },
        sFofE: function() { with(smoothFrame.shortcuts){ return sFo().frameElement; } }
    },
    options : {
        css : 'body { overflow: hidden }',
        sourceElement: { 
            selector:  '#blogs',
            trigger: {
                selector : 'a'
            },
            effect: {
                toggle : true
            },
            htmlSetup : null
        },
        frameElement: { 
            containerSelector:  '.iframe-box',
            selector: function() { 
                with(smoothFrame.shortcuts){
                     return sFofE().containerSelector + ' iframe';
                }
            },
            doAnimation: true,
            /* optional target url with placeholder */
            targetUrlwPlh: null,
            css : { 
                iframe: { top : '15.7%', padding: '0' },
                closeLink : { cursor : 'pointer' }
            },
            animate : {
                iframe : {
                    height: '+=62em',
                    width: '+=42%',
                    left : '0',
                    top: '0'
                },
                closeLink : {
                    width:'+=40%',
                    left:'-5px', 
                    top:'-20px'
                }
            }
        }
    },
    setup : function(){
        with(smoothFrame.shortcuts){
            /* css setup */
            var script = document.createElement('script');
            script.type = 'text/css';
            script.innerHTML = sFo().css;
            document.getElementsByTagName('head')[0].appendChild(script);

            /* source element html setup */
            if (sFosE().htmlSetup){
                sFosE().htmlSetup();
            }

            /* source element links binding */
            $(sFosE().selector + ' ' 
                + sFosE().trigger.selector
            ).bind('click', sF().openFrame)

            /* Elements */
            /* a close */
            var aClose = document.createElement('a');
            aClose.className = 'close position-absolute display-block width60pc text-alignr bold';
            aClose.innerHTML = 'close';
            $(aClose).css(sFofE().css.closeLink);
            $(aClose).bind('click', sF().closeFrame);
            /* iframe */
            var iframe = document.createElement('iframe');
            iframe.id = 'iframe';
            iframe.name = 'iframe';
            iframe.className = "position-absolute width60pc margin-auto";
            $(iframe).css(sFofE().css.iframe);
            /* append */
            $(sFofE().containerSelector).append(aClose);
            $(sFofE().containerSelector).append(iframe);

            /* show/hide element links */
            var aShow = document.createElement('a');
            var aHide = document.createElement('a');
            aShow.href = 'javascript:$("'+sFofE().selector()+'").show("slow");';
            aHide.href = 'javascript:$("'+sFofE().selector()+'").hide();';
            $(aShow).addClass("color-transparent");
            $(aHide).addClass("color-transparent");
            $(aShow).html('show');
            $(aHide).html('hide');

            $(sFofE().containerSelector).after(aHide);
            $(sFofE().containerSelector).after(aShow);
        }   
    },
    openFrame : function(e){
        with(smoothFrame.shortcuts){
            if (sFosE().effect.toggle){
                $(sFosE().selector).animate({opacity:0.2});
            }

            if (sFofE().targetUrlwPlh){
                $(sFofE().selector())[0].src =
                    sFofE().targetUrlwPlh.replace(
                        '%plh',
                        e.srcElement.href.split('#')[1]
                    );
            }
            else {
                $(sFofE().selector())[0].src = e.srcElement.href;
            }
            $(sFofE().containerSelector).show();
            if (sFofE().doAnimation){
                $(sFofE().containerSelector +' a.close').animate(
                    {
                        width:sFofE().animate.closeLink.width,
                        left:sFofE().animate.closeLink.left, 
                        top:sFofE().animate.closeLink.top
                    }
                );
                $(sFofE().selector()).animate(
                    {
                        height:sFofE().animate.iframe.height,
                        width:sFofE().animate.iframe.width,
                        left:sFofE().animate.iframe.left,
                        top:sFofE().animate.iframe.top
                    },
                    1000,
                    function(){
                    // pass
                    }
                );
                sFofE().doAnimation = false;
            }
        }
        e.preventDefault();
    },
    closeFrame: function(e){
        with(smoothFrame.shortcuts){
            if (sFosE().effect.toggle){
                $(sFosE().selector).animate({opacity:1}, 1000);
            }
            $(sFofE().selector())[0].src='';
            $(sFofE().containerSelector).hide();
        }
    }
}
