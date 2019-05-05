function initStreamform(){
    $('[data-conditional-target-name]').each(function(index, value){

        conditional_input_name = $(value).data('conditional-target-name');
        conditional_input_value = $(value).data('conditional-target-value');
        conditional_input = $('[data-conditional-name=' + conditional_input_name + '] input');
        setInitial(conditional_input, conditional_input_value, value);
        setTriggers(conditional_input, conditional_input_value, value);
    })
};

function setTriggers(conditional_input, conditional_input_value, target_element){

    conditional_input.bind('input', function(){
        if($(this).val() == conditional_input_value){
            $(target_element).show();
        } else {
            $(target_element).hide();
        }
    });
}

function setInitial(conditional_input, conditional_input_value, target_element){
    if($(conditional_input).val() == conditional_input_value){
        $(target_element).show();
    } else {
        $(target_element).hide();
    }
}