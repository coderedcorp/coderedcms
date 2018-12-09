$(document).ready(function() {
    $.ajax({
        url: '/cms/versions.txt',
        success: function(data) {
            data.split('\n').forEach((item, index) => {
                if(item.trim() != '') {
                    newa = document.createElement('a', );
                    newa.setAttribute('href', '/cms/' + item + '/');
                    newa.innerHTML = item;
                    document.getElementById("other-versions").appendChild(newa);
                }
            }
        )}
    });
});