jQuery(document).ready(function($){
    $("#question-list .question a, td.link-external a, .link-external").attr('target', '_blank');
    
    $("select, input:checkbox, input:radio, input:file, input:submit").uniform();	
    
    $(".close").click(function(){
        $(this).parent().parent().slideUp();
    });
    
    
    function gen_chart(){
        var total = parseInt($("aside#cluster-summary-side .chart div").attr("id"));
        var analyzed = parseInt($("aside#cluster-summary-side .chart div span").attr("id"));
        var p;
        
        p = (analyzed * 100)/total;
    
        $("aside#cluster-summary-side .chart div span").css("width", p +'%');
        $("aside#cluster-summary-side .chart div").append(p + '%');
    }
    if($("aside#cluster-summary-side .chart").length > 0){
        gen_chart();
    }
    
    
    if($("#id_cluster_filter").length){
        $("#id_cluster_filter").change(function(){
            document.location.href = $(this).val();
        });
    }
    
    $("nav.hor-menu li").mouseover(function(){
        $(this).find("ul").show();
    });
    
    $("nav.hor-menu li ul").mouseout(function(){
        $(this).hide();
    });
    
    
    $(".confirm").click(function(){
        if(confirm('Deseja mesmo remover este item?\nNão será possível desfazer esta operação.')){
            return true;
        }
        return false;
    });
    
    $(".show-sequence").click(function(){
        $(this).fadeOut('fast', function(){
            $("#sequence-container").slideDown();            
        });
    });
    
    $(".hide-sequence").click(function(){
        $("#sequence-container").slideUp(function(){
            $(".show-sequence").fadeIn();
        });            

    });
    
    $("#lang-pt-br").click(function(){
        $("#next-lang").val('pt-br');
        $(this).parent().submit();
    });

    $("#lang-en-us").click(function(){
        $("#next-lang").val('en');
        $(this).parent().submit();
    });

});