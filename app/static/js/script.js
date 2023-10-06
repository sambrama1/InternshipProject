
function getCookie(name){
    let cookieValue = null;
    if (document.cookie && document.cookie !== ""){
        const cookies = document.cookie.split(";");
        for(let i=0;i<cookies.length; i++){
            const cookie = cookies[i].trim();
            if(cookie.substring(0, name.length + 1) === (name + "=")){
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
  return cookieValue;
}


$(document).ready(function () {
    $('.plusCart').click(function () {
        console.log('plusCart');
        var id = $(this).attr("pid");
        var tableNumber = $(this).data("table");
        console.log('tableno',tableNumber)

        var eml = $(this).parent().children().eq(2);

        console.log(id);

        $.ajax({
            type: "POST",
            url: '/plusCart/',
            dataType: "json",
            data: {
                dish_id: id,
                table_number: tableNumber,
            },
            headers: {
                "X-Requested-with": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            success: function (data) {
                eml.text(data.quantity); 
                $("#amount").text(data.amount); 
                $("#totalamount").text(data.totalamount);
            }
        });
    });
});


$(document).ready(function () {
    $('.minusCart').click(function () {
        console.log('minusCart');
        var id = $(this).attr("pid");
        var tableNumber = $(this).data("table");
        console.log('tableno',tableNumber)

        var eml = $(this).parent().children().eq(2);
        console.log(id);

        $.ajax({
            type: "POST",
            url: '/minusCart/',
            dataType: "json",
            data: {
                dish_id: id,
                table_number: tableNumber,
            },
            headers: {
                "X-Requested-with": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            success: function (data) {
                eml.text(data.quantity); 
                $("#amount").text(data.amount); 
                $("#totalamount").text(data.totalamount);
            }
        });
    });
});

$(document).ready(function () {
    $('.removeCart').click(function () {
        console.log('removeCart');
        var id = $(this).attr("pid"); 
        var tableNumber = $(this).data("table");
        console.log('tableno',tableNumber)
        var eml = $(this).parent().parent().find('.quantity'); 
        console.log(id);

        $.ajax({
            type: "POST",
            url: '/removeCart/',
            dataType: "json",
            data: {
                dish_id: id,
                table_number: tableNumber,
                
            },
            headers: {
                "X-Requested-with": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            success: function (data) {
                eml.text(data.quantity); 
                $("#amount").text(data.amount); 
                $("#totalamount").text(data.totalamount); 
            }
        });
    });
});