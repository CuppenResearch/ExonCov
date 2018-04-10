"""ExonCov admin views."""
from flask_admin.contrib.sqla import ModelView

from . import db, admin
from .models import Exon, Transcript, Gene, Panel, Sample, SequencingRun


class CustomModelView(ModelView):
    """Create customized default model view class."""

    can_delete = False

    # Required for flask-login implementation -> depends on authorization method
    # def is_accessible(self):
    #     """Check whether user has acces to admin panel."""
    #     if not current_user.is_active or not current_user.is_authenticated:
    #         return False
    #
    #     if current_user.has_role('admin'):
    #         return True
    #
    #     return False
    #
    # def _handle_view(self, name, **kwargs):
    #     """Redirect users when a view is not accessible."""
    #     if not self.is_accessible():
    #         if current_user.is_authenticated:
    #             # permission denied
    #             abort(403)
    #         else:
    #             # login
    #             return redirect(url_for('security.login', next=request.url))


class PanelAdminView(CustomModelView):
    """Panel admin view."""
    column_searchable_list = ['name']

    form_columns = ['name', 'transcripts']
    form_ajax_refs = {
        'transcripts': {
            'fields': ['name', 'gene_id'],
            'page_size': 10
        }
    }


class GeneAdminView(CustomModelView):
    """Gene admin view."""
    column_list = ['id', 'default_transcript']
    column_sortable_list = ['id']
    column_searchable_list = ['id']


    form_columns = ['id', 'transcripts', 'default_transcript']
    form_ajax_refs = {
        'transcripts': {
            'fields': ['name'],
            'page_size': 10
        },
        'default_transcript': {
            'fields': ['name'],
            'page_size': 10
        }
    }


class TranscriptAdminView(CustomModelView):
    """Transcript admin view."""
    column_list = ['name', 'chr', 'start', 'end', 'gene']
    column_sortable_list = ['name', 'chr', 'start', 'end']
    column_searchable_list = ['name', 'gene_id']
    column_filters = ['chr', 'start', 'end']

    form_columns = ['name', 'gene', 'exons', 'chr', 'start', 'end']  # Automatically set chr, start, end based on exons.
    form_ajax_refs = {
        'gene': {
            'fields': ['id'],
            'page_size': 10
        },
        'exons': {
            'fields': ['id'],
            'page_size': 10
        }
    }


class ExonAdminView(CustomModelView):
    """Exon admin view."""
    column_list = ['chr', 'start', 'end']
    column_sortable_list = ['chr', 'start', 'end']
    column_filters = ['chr', 'start', 'end']

    form_columns = ['chr', 'start', 'end']


class SampleAdminView(CustomModelView):
    """Sample admin view."""
    column_list = ['name', 'sequencing_run', 'import_date']
    column_sortable_list = ['name', 'import_date']
    column_searchable_list = ['name']

    form_columns = ['name', 'sequencing_run', 'import_date']
    form_ajax_refs = {
        'sequencing_run': {
            'fields': ['name'],
            'page_size': 10
        },
    }


class SequencingRunAdminView(CustomModelView):
    """SequencingRun admin view."""
    column_list = ['name', 'sequencer']
    column_sortable_list = ['name', 'sequencer']
    column_searchable_list = ['name', 'sequencer']

    form_columns = ['name', 'sequencer']
    form_choices = {
        'sequencer': [
            ('nextseq_umc01', 'Nextseq UMC01'),
            ('nextseq_umc02', 'Nextseq UMC02'),
            ('novaseq_umc01', 'Novaseq UMC01')
        ],
    }


# Link view classes and models
admin.add_view(PanelAdminView(Panel, db.session))
admin.add_view(GeneAdminView(Gene, db.session))
admin.add_view(TranscriptAdminView(Transcript, db.session))
admin.add_view(ExonAdminView(Exon, db.session))
admin.add_view(SampleAdminView(Sample, db.session))
admin.add_view(SequencingRunAdminView(SequencingRun, db.session))
