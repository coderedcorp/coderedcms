from django import forms


class ColorPickerWidget(forms.TextInput):
    input_type = 'color'


class ClassifierSelectWidget(forms.CheckboxSelectMultiple):
    template_name = 'coderedcms/widgets/checkbox_classifiers.html'

    def optgroups(self, name, value, attrs=None):
        from coderedcms.models.snippet_models import Classifier
        classifiers = Classifier.objects.all().select_related()

        groups = []
        has_selected = False

        for index, classifier in enumerate(classifiers):
            subgroup = []
            group_name = classifier.name
            subindex = 0
            choices = []

            for term in classifier.terms.all():
                choices.append((term.pk, term.name))

            groups.append((group_name, subgroup, index))

            for subvalue, sublabel in choices:
                selected = (
                    str(subvalue) in value and
                    (not has_selected or self.allow_multiple_selected)
                )
                has_selected |= selected
                subgroup.append(self.create_option(
                    name, subvalue, sublabel, selected, index,
                    subindex=subindex, attrs=attrs,
                ))
                if subindex is not None:
                    subindex += 1
        return groups
