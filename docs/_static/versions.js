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
    if(sessionStorage.getItem(vfile)) {
        setversions(sessionStorage.getItem(vfile));
    }
    else {
        $.ajax({
            url: vroot + vfile,
            success: function(data) {
                sessionStorage.setItem(vfile, data);
                setversions(data);
            }
        });
    }
});