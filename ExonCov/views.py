"""ExonCov views."""

from flask import render_template

from ExonCov import app, db
from .models import Sample, Panel, Gene, Transcript, Exon, ExonMeasurement, TranscriptMeasurement, panels_transcripts, exons_transcripts


@app.route('/')
@app.route('/sample')
def samples():
    """Sample overview page."""
    samples = Sample.query.all()
    return render_template('samples.html', samples=samples)


@app.route('/sample/<int:id>')
def sample(id):
    """Sample page."""
    sample = Sample.query.get(id)
    measurement_types = ['measurement_mean_coverage', 'measurement_percentage15', 'measurement_percentage30']
    query = db.session.query(Panel.name, TranscriptMeasurement).join(Transcript, Panel.transcripts).join(TranscriptMeasurement).filter_by(sample_id=sample.id).all()
    panels = {}

    for panel_name, transcript_measurement in query:
        if panel_name not in panels:
            panels[panel_name] = {
                'len': transcript_measurement.len
            }
            for measurement_type in measurement_types:
                panels[panel_name][measurement_type] = transcript_measurement[measurement_type]
        else:
            for measurement_type in measurement_types:
                panels[panel_name][measurement_type] = ((panels[panel_name]['len'] * panels[panel_name][measurement_type]) + (transcript_measurement.len * transcript_measurement[measurement_type])) / (panels[panel_name]['len'] + transcript_measurement.len)
            panels[panel_name]['len'] += transcript_measurement.len
    return render_template('sample.html', sample=sample, panels=panels, measurement_types=measurement_types)


@app.route('/sample/<int:sample_id>/panel/<string:panel_name>')
def sample_panel(sample_id, panel_name):
    """Sample panel page."""
    sample = Sample.query.get(sample_id)
    panel = Panel.query.filter_by(name=panel_name).first()

    measurement_types = ['measurement_mean_coverage', 'measurement_percentage15', 'measurement_percentage30']
    transcript_measurements = db.session.query(Transcript, TranscriptMeasurement).join(panels_transcripts).filter(panels_transcripts.columns.panel_id == panel.id).join(TranscriptMeasurement).filter_by(sample_id=sample.id).all()

    return render_template('sample_panel.html', sample=sample, panel=panel, transcript_measurements=transcript_measurements, measurement_types=measurement_types)


@app.route('/sample/<int:sample_id>/transcript/<string:transcript_name>')
def sample_transcript(sample_id, transcript_name):
    """Sample transcript page."""
    sample = Sample.query.get(sample_id)
    transcript = Transcript.query.filter_by(name=transcript_name).first()

    measurement_types = ['measurement_mean_coverage', 'measurement_percentage15', 'measurement_percentage30']
    exon_measurements = db.session.query(Exon, ExonMeasurement).join(exons_transcripts).filter(exons_transcripts.columns.transcript_id == transcript.id).join(ExonMeasurement).filter_by(sample_id=sample.id).all()

    return render_template('sample_transcript.html', sample=sample, transcript=transcript, exon_measurements=exon_measurements, measurement_types=measurement_types)


@app.route('/sample/<int:sample_id>/gene/<string:gene_id>')
def sample_gene(sample_id, gene_id):
    """Sample gene page."""
    sample = Sample.query.get(sample_id)
    gene = Gene.query.get(gene_id)

    measurement_types = ['measurement_mean_coverage', 'measurement_percentage15', 'measurement_percentage30']
    transcript_measurements = db.session.query(Transcript, TranscriptMeasurement).filter(Transcript.gene_id == gene.id).join(TranscriptMeasurement).filter_by(sample_id=sample.id).all()

    return render_template('sample_gene.html', sample=sample, gene=gene, transcript_measurements=transcript_measurements, measurement_types=measurement_types)
