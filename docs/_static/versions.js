vroot = '/cms/';
vfile = 'versions.txt';

function setversions(data) {
    data.split('\n').forEach((item, index) => {
        if(item.trim() != '') {
            newa = document.createElement('a', );
            newa.setAttribute('href', vroot + item + '/');
            newa.innerHTML = item;
            document.getElementById("other-versions").appendChild(newa);
        }
    });
}

$(document).ready(function() {
    if(sessionStorage.getItem(vroot+vfile)) {
        setversions(sessionStorage.getItem(vroot+vfile));
    }
    else {
        $.ajax({
            url: vroot + vfile,
            success: function(data) {
                sessionStorage.setItem(vroot+vfile, data);
                setversions(data);
            }
        });
    }
});