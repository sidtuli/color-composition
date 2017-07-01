$.getJSON('test.txt', function(data) {
        
    console.log(data);
    $(document.body).append("<img src='flags-ultra/"+Object.keys(data)[1]+"'>");
    $(document.body).append(String(data[Object.keys(data)[1]]))
    console.log(data[Object.keys(data)[1]])
});