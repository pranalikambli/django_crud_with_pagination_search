$(function(){
    $('.alert').delay(3000).fadeOut();
    $('#delete_success').delay(3000).fadeOut();
    $("input[name=filter]").on('keyup keypress', function(e) {
        var keyCode = e.keyCode || e.which;
        if (keyCode === 13) {
        e.preventDefault();
        return false;
        }
     });
    $(".search").keyup(function(){
		var url = '/list'; // Backend url
		var params = {'filter':$("input[name=filter]").val(), 'sortfn':$("input[name=sortfn]").val(), 'sortln':$("input[name=sortln]").val(), 'sortemail':$("input[name=sortemail]").val(), 'sortage':$("input[name=sortage]").val(), 'click':$("input[name=click]").val()}; // Search field value
		fetchData(url, params); // Backend call for filtered data
	}).trigger('keyup');
});

function fetchData(url, params) {

    var sortbyfn = $("#sortbyfn").val();
    var sortbyln = $("#sortbyln").val();
    var sortbyemail = $("#sortbyemail").val();
    var sortbyage = $("#sortbyage").val();
    $.get(url, params)
    .done(function(data){
        // Put the data into target div
        $("#results").html(data);
        var sortbyfn = $("#sortbyfn").val();
           sortbycharfn=sortbyfn.substring(0,1)
           sortbycharln=sortbyln.substring(0,1)
           sortbycharemail=sortbyemail.substring(0,1)
           sortbycharage=sortbyage.substring(0,1)

           if(sortbycharfn =="-")
           {
                $(".fn").removeClass("main");
           }
           else
           {
                $(".fn").toggleClass("main");
           }
           if(sortbycharln =="-")
           {
                $(".ln").removeClass("main");
           }
           else
           {
                $(".ln").toggleClass("main");
           }
           if(sortbycharemail =="-")
           {
                $(".email").removeClass("main");
           }
           else
           {
                $(".email").toggleClass("main");
           }
           if(sortbycharage =="-")
           {
                $(".age").removeClass("main");
           }
           else
           {
                $(".age").toggleClass("main");
           }

		    $(".fn").click(function(){
              $(".fn").toggleClass("main");
               var sortbyfn = $("#sortbyfn").val();
               var click = $("#click").val(1);
               sortbycharfn=sortbyfn.substring(0,1)
               if(sortbycharfn =="-")
               {
                    sortbyfn=sortbyfn.substring(1);
                    $("#sortbyfn").val(sortbyfn);
                    $("#click").val(1);
               }
               else
               {
                 sortbyfn ="-"+sortbyfn;
                 $("#sortbyfn").val(sortbyfn);
                 $("#click").val(1);
               }
               var url = '/list';
               var params = {'filter':$("input[name=filter]").val(),'sortfn':$("input[name=sortfn]").val(),'sortln':$("input[name=sortln]").val(), 'sortemail':$("input[name=sortemail]").val(), 'sortage':$("input[name=sortage]").val(), 'click':$("input[name=click]").val()};
               fetchData(url, params);

            });
            $(".ln").click(function(){
              $(".ln").toggleClass("main");
               var sortbyln = $("#sortbyln").val();
               sortbycharln=sortbyln.substring(0,1)
               if(sortbycharln =="-")
               {
                    sortbyln=sortbyln.substring(1);
                    $("#sortbyln").val(sortbyln);
                    $("#click").val(2);
               }
               else{
                sortbyln ="-"+sortbyln;
                 $("#sortbyln").val(sortbyln);
                 $("#click").val(2);
               }
               var url = '/list'; // Backend url
               var params = {'filter':$("input[name=filter]").val(),'sortfn':$("input[name=sortfn]").val(),'sortln':$("input[name=sortln]").val(), 'sortemail':$("input[name=sortemail]").val(), 'sortage':$("input[name=sortage]").val(), 'click':$("input[name=click]").val()}; // Search field value
               fetchData(url, params);

            });
            $(".email").click(function(){
              $(".email").toggleClass("main");
               var sortbyemail = $("#sortbyemail").val();
               sortbycharemail=sortbyemail.substring(0,1)
               if(sortbycharemail =="-")
               {
                    sortbyemail=sortbyemail.substring(1);
                    $("#sortbyemail").val(sortbyemail);
                    $("#click").val(3);
               }
               else{
                sortbyemail ="-"+sortbyemail;
                 $("#sortbyemail").val(sortbyemail);
                 $("#click").val(3);
               }
               var url = '/list'; // Backend url
               var params = {'filter':$("input[name=filter]").val(),'sortfn':$("input[name=sortfn]").val(),'sortln':$("input[name=sortln]").val(), 'sortemail':$("input[name=sortemail]").val(), 'click':$("input[name=click]").val()}; // Search field value
               fetchData(url, params);

            });
            $(".age").click(function(){
              $(".lagen").toggleClass("main");
               var sortbyage = $("#sortbyage").val();
               sortbycharage=sortbyage.substring(0,1)
               if(sortbycharage =="-")
               {
                    sortbyage=sortbyage.substring(1);
                    $("#sortbyage").val(sortbyage);
                    $("#click").val(4);
               }
               else{
                sortbyage ="-"+sortbyage;
                 $("#sortbyage").val(sortbyage);
                 $("#click").val(4);
               }
               var url = '/list'; // Backend url
               var params = {'filter':$("input[name=filter]").val(),'sortfn':$("input[name=sortfn]").val(),'sortln':$("input[name=sortln]").val(), 'sortemail':$("input[name=sortemail]").val(), 'sortage':$("input[name=sortage]").val(), 'click':$("input[name=click]").val()}; // Search field value
               fetchData(url, params);

            });
        // Get next page on navigation button click
        $(".previous, .next").click(function(elem){
            // Prevent button from taking you away from current page
            elem.preventDefault();
            // Get the page's url from the button clicked
            var url = '/list' + $(this).attr('href');

            // Call this function again with url containing page parameter
            fetchData(url, params);
        });
    });
};
function showdelete(name,id)
{
    $('#autoid').val(id);
    $('#deleting_field').html(name);
    $('#myModal').modal('show');
}

function deleteemp()
{
    var deleteid= $('#autoid').val();
    url='/delete/'+deleteid;
    $.ajax({
            type: 'GET',
            url:url,
            dataType: 'json',

            success: function(data) {

            if(data.message ==0)
            {
                alert('Something Went Wrong');
            }
            else
            {
                $('#myModal').modal('hide');
                $("#delete_success").show();
                $('#delete_success').delay(3000).fadeOut();

               $("input[name=filter]").keyup(function(){
                    var url = '/list';
                    var params = {'filter':$("input[name=filter]").val()};
                    fetchData(url, params);
               }).trigger('keyup');
            }
            },
            error: function(data) { // if error occured
                alert("Error occured.please try again");
            }
    });
}