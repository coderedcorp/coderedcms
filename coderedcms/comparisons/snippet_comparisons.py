from django.shortcuts import get_object_or_404
from django.utils.html import format_html
from django.utils.html import format_html_join

from wagtail.admin.compare import (
    BlockComparison,
    get_comparison_class_for_block,
)

from wagtail.admin.panels import get_edit_handler


class ReusableContentComparison(BlockComparison):
    def get_revision(self, val):
        instance = val["content"]
        revision_id = val["revision"]
        revision = get_object_or_404(instance.revisions, id=revision_id)
        return revision.as_object()

    def htmldiff(self):
        htmldiffs = []
        for name, block in self.block.child_blocks.items():
            label = self.block.child_blocks[name].label

            if name == "revision":
                # Ignore this field, we don't want to display diffs for it.
                continue

            elif name == "content":
                instance = self.val_a["content"]
                revision_a = self.get_revision(self.val_a)
                revision_b = self.get_revision(self.val_b)

                # Copied from with modifications:
                # https://github.com/wagtail/wagtail/blob/
                # 9edaadaef094d7732025121c32313472b353ace8/
                # wagtail/admin/views/generic/models.py#L739-L752
                comparison = (
                    get_edit_handler(self.val_a["content"])
                    .get_bound_panel(instance=instance)
                    .get_comparison()
                )

                for comp in comparison:
                    diff = comp(revision_a, revision_b)
                    if diff.has_changed():
                        htmldiffs.append(
                            (
                                instance._meta.verbose_name,
                                diff.htmldiff(),
                            )
                        )

            else:
                comparison_class = get_comparison_class_for_block(block)

                htmldiffs.append(
                    (
                        label,
                        comparison_class(
                            block,
                            self.exists_a,
                            self.exists_b,
                            self.val_a[name],
                            self.val_b[name],
                        ).htmldiff(),
                    )
                )

        return format_html(
            "<dl>\n{}\n</dl>",
            format_html_join(
                "\n",
                "    <dt>{}</dt>\n    <dd>{}</dd>",
                htmldiffs,
            ),
        )
