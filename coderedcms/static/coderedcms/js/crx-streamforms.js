condition_triggered = function ($source_field, $target_field) {
  // Custom logic for checkboxes since `.val()` always returns a fixed value,
  // :checked property must be evaluated instead.
  if ($source_field.prop("type") == "checkbox") {
    $source_field.each(function () {
      var $source_field = $(this);
      $trigger_checkbox = $source_field.closest(
        "[value='" + $target_field.data("condition-trigger-value") + "']"
      );
      if ($trigger_checkbox.length > 0) {
        if ($trigger_checkbox.prop("checked")) {
          $target_field.show();
        } else {
          $target_field.hide();
        }
      }
    });
  } else {
    if (
      $source_field.val().trim() ==
      $target_field.data("condition-trigger-value").trim()
    ) {
      $target_field.show();
    } else {
      $target_field.hide();
    }
  }
};

$("[data-condition-trigger-id]").each(function () {
  // Get source/target fields from data attributes.
  var $target_field = $(this);
  var source_query = "#" + $(this).data("condition-trigger-id");
  var $source_field = $(
    source_query +
      " input, " +
      source_query +
      " textarea, " +
      source_query +
      " select"
  );
  var source_field_name = $source_field.prop("name");

  // Trigger initial state of input.
  condition_triggered($source_field, $target_field);

  // Watch change event for similarly named inputs within this form. It is
  // necessary to watch based on name because selecting another radio button
  // does not trigger a `change` for other radio buttons, it only triggers a
  // change for the whole radio group (identified by "name").
  var $form = $(this).closest("form");
  $form.find("[name='" + source_field_name + "']").change(function () {
    condition_triggered($(this), $target_field);
  });
});
