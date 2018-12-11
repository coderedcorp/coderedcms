vfile = '/cms/versions.txt';

function setversions(data) {
    data.split('\n').forEach((item, index) => {
        if(item.trim() != '') {
            newa = document.createElement('a', );
            newa.setAttribute('href', '/cms/' + item + '/');
            newa.innerHTML = item;
            document.getElementById("other-versions").appendChild(newa);
        }
    });
}

$(document).ready(function() {
    if(sessionStorage.getItem(vfile)) {
        setversions(sessionStorage.getItem(vfile));
    }
    else {
        $.ajax({
            url: '/cms/versions.txt',
            success: function(data) {
                sessionStorage.setItem(vfile, data);
                setversions(data);
            }
        });
    }
});