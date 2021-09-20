jQuery(function($){
    $(document).ready(function(){
        $("#id_product_enterprsie").change(function(){
            $.ajax({
                url:'/category/',
                type:"POST",
                data:{
                    'product_enterprsie': $('#id_product_enterprsie').val(),
                    'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
                },
                success: function(result) {
                    console.log(result);
                    cols = document.getElementById("id_product_categories");
                    cols.options.length = 0;
                    for(var k in result){
                        cols.options.add(new Option(k, result[k]));
                    }
                },
                // error: function(e){
                //     console.error(JSON.stringify(e));
                // },
            });
        });
    }); 
});