import csv
import logging
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.schema import CreateSchema, DropSchema
from itertools import zip_longest
from django.conf import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from glob import glob
from .contextual import contextual_rows
from collections import defaultdict


logger = logging.getLogger("rainbow")
Base = declarative_base()
SCHEMA = 'otu'


# from itertools recipes
def grouper(iterable, n):
    "Collect data into fixed-length chunks or blocks"
    args = [iter(iterable)] * n
    return zip_longest(*args)


class SchemaMixin():
    """
    we use a specific schema (rather than the public schema) so that the import
    can be easily re-run, simply by deleting the schema. this also keeps
    SQLAlchemy tables out of the way of Django tables, and vice-versa
    """
    __table_args__ = {
        "schema": SCHEMA
    }


class OntologyMixin(SchemaMixin):
    id = Column(Integer, primary_key=True)
    value = Column(String, unique=True)

    @classmethod
    def make_tablename(cls, name):
        return 'ontology_' + name.lower()

    @declared_attr
    def __tablename__(cls):
        return cls.make_tablename(cls.__name__)

    def __repr__(self):
        return "<%s(%s)>" % (type(self).__name__, self.value)


def ontology_fkey(nm):
    return Column(Integer, ForeignKey(SCHEMA + '.' + OntologyMixin.make_tablename(nm) + '.id'))


class OTUKingdom(OntologyMixin, Base):
    pass


class OTUPhylum(OntologyMixin, Base):
    pass


class OTUClass(OntologyMixin, Base):
    pass


class OTUOrder(OntologyMixin, Base):
    pass


class OTUFamily(OntologyMixin, Base):
    pass


class OTUGenus(OntologyMixin, Base):
    pass


class OTUSpecies(OntologyMixin, Base):
    pass


class OTU(SchemaMixin, Base):
    __tablename__ = 'otu'
    id = Column(Integer, primary_key=True)
    code = Column(String(length=21))  # current max length of OTU code
    kingdom_id = ontology_fkey('OTUKingdom')
    phylum_id = ontology_fkey('OTUPhylum')
    class_id = ontology_fkey('OTUClass')
    order_id = ontology_fkey('OTUOrder')
    family_id = ontology_fkey('OTUFamily')
    genus_id = ontology_fkey('OTUGenus')
    species_id = ontology_fkey('OTUSpecies')
    kingdom = relationship(OTUKingdom)
    phylum = relationship(OTUPhylum)
    klass = relationship(OTUClass)
    order = relationship(OTUOrder)
    family = relationship(OTUFamily)
    species = relationship(OTUSpecies)


class SampleHorizonClassification(OntologyMixin, Base):
    pass


class SampleStorageMethod(OntologyMixin, Base):
    pass


class SampleLandUse(OntologyMixin, Base):
    pass


class SampleEcologicalZone(OntologyMixin, Base):
    pass


class SampleVegetationType(OntologyMixin, Base):
    pass


class SampleProfilePosition(OntologyMixin, Base):
    pass


class SampleAustralianSoilClassification(OntologyMixin, Base):
    pass


class SampleFAOSoilClassification(OntologyMixin, Base):
    pass


class SampleTillage(OntologyMixin, Base):
    pass


class SampleColor(OntologyMixin, Base):
    pass


class SampleContext(SchemaMixin, Base):
    __tablename__ = 'sample_context'
    id = Column(Integer, primary_key=True)  # NB: we use the final component of the BPA ID here
    date_sampled = Column(Date)
    latitude = Column(Float)
    longitude = Column(Float)
    depth = Column(Float)
    geo_loc_name = Column(String)
    location_description = Column(String)
    vegetation_total_cover = Column(Float)
    vegetation_dom_trees = Column(Float)
    vegetation_dom_shrubs = Column(Float)
    vegetation_dom_grasses = Column(Float)
    elevation = Column(Float)
    slope = Column(String)
    slope_aspect = Column(String)
    date_since_change_in_land_use = Column(String)
    crop_rotation_1yr_since_present = Column(String)
    crop_rotation_2yrs_since_present = Column(String)
    crop_rotation_3yrs_since_present = Column(String)
    crop_rotation_4yrs_since_present = Column(String)
    crop_rotation_5yrs_since_present = Column(String)
    agrochemical_additions = Column(String)
    fire_history = Column(String)
    fire_intensity_if_known = Column(String)
    flooding = Column(String)
    extreme_events = Column(String)
    soil_moisture = Column(Float)
    gravel = Column(Float)
    texture = Column(Float)
    course_sand = Column(Float)
    fine_sand = Column(Float)
    sand = Column(Float)
    silt = Column(Float)
    clay = Column(Float)
    ammonium_nitrogen = Column(Float)
    nitrate_nitrogen = Column(Float)
    phosphorus_colwell = Column(Float)
    potassium_colwell = Column(Float)
    sulphur = Column(Float)
    organic_carbon = Column(Float)
    conductivity = Column(Float)
    ph_level_cacl2 = Column(Float)
    ph_level_h2o = Column(Float)
    dtpa_copper = Column(Float)
    dtpa_iron = Column(Float)
    dtpa_manganese = Column(Float)
    dtpa_zinc = Column(Float)
    exc_aluminium = Column(Float)
    exc_calcium = Column(Float)
    exc_magnesium = Column(Float)
    exc_potassium = Column(Float)
    exc_sodium = Column(Float)
    boron_hot_cacl2 = Column(Float)
    #
    horizon_classification_id = ontology_fkey('SampleHorizonClassification')
    soil_sample_storage_method_id = ontology_fkey('SampleStorageMethod')
    broad_land_use_id = ontology_fkey('SampleLandUse')
    detailed_land_use_id = ontology_fkey('SampleLandUse')
    general_ecological_zone_id = ontology_fkey('SampleEcologicalZone')
    vegetation_type_id = ontology_fkey('SampleVegetationType')
    profile_position_id = ontology_fkey('SampleProfilePosition')
    australian_soil_classification_id = ontology_fkey('SampleAustralianSoilClassification')
    fao_soil_classification_id = ontology_fkey('SampleFAOSoilClassification')
    immediate_previous_land_use_id = ontology_fkey('SampleLandUse')
    tillage_id = ontology_fkey('SampleTillage')
    color_id = ontology_fkey('SampleColor')


class SampleOTU(SchemaMixin, Base):
    __tablename__ = 'sample_otu'
    sample_id = Column(Integer, ForeignKey(SCHEMA + '.sample_context.id'), primary_key=True)
    otu_id = Column(Integer, ForeignKey(SCHEMA + '.otu.id'), primary_key=True)
    count = Column(Integer, nullable=False)


def make_engine():
    conf = settings.DATABASES['default']
    engine_string = 'postgres://%(USER)s:%(PASSWORD)s@%(HOST)s:%(PORT)s/%(NAME)s' % (conf)
    return create_engine(engine_string)


class DataImporter:
    def __init__(self, import_base):
        self._engine = make_engine()
        Session = sessionmaker(bind=self._engine)
        self._session = Session()
        self._import_base = import_base
        try:
            self._session.execute(DropSchema(SCHEMA, cascade=True))
        except sqlalchemy.exc.ProgrammingError:
            self._session.invalidate()
        self._session.execute(CreateSchema(SCHEMA))
        self._session.commit()
        Base.metadata.create_all(self._engine)

    def _read_tab_file(self, fname):
        with open(fname) as fd:
            reader = csv.DictReader(fd, dialect="excel-tab")
            yield from reader

    def _build_ontology(self, db_class, vals):
        for val in vals:
            instance = db_class(value=val)
            self._session.add(instance)
        self._session.commit()
        return dict((t.value, t.id) for t in self._session.query(db_class).all())

    def _load_ontology(self, ontology_defn, rows):
        # import the ontologies, and build a mapping from
        # permitted values into IDs in those ontologies
        by_class = defaultdict(list)
        for field, db_class in ontology_defn.items():
            by_class[db_class].append(field)

        mappings = {}
        for db_class, fields in by_class.items():
            vals = set()
            for row in rows:
                for field in fields:
                    if field in row:
                        vals.add(row[field])
            map_dict = self._build_ontology(db_class, vals)
            for field in fields:
                mappings[field] = map_dict
        return mappings

    def load_taxonomies(self):
        logger.warning("loading taxonomies")

        # load each taxnomy file. note that not all files
        # have all of the columns
        rows = []
        for fname in glob(self._import_base + '/*.taxonomy'):
            rows += list(self._read_tab_file(fname))
        ontologies = {
            'kingdom': OTUKingdom,
            'phylum': OTUPhylum,
            'class': OTUClass,
            'order': OTUOrder,
            'family': OTUFamily,
            'genus': OTUGenus,
            'species': OTUSpecies
        }
        mappings = self._load_ontology(ontologies, rows)

        def _make_otus():
            for row in rows:
                attrs = {}
                for field in ontologies:
                    if field not in row:
                        continue
                    attrs[field + '_id'] = mappings[field][row[field]]
                yield OTU(code=row['OTUId'], **attrs)
        # import the OTU rows, applying ontology mappings
        self._session.bulk_save_objects(_make_otus())
        self._session.commit()

    def load_contextual_metadata(self):
        logger.warning("loading contextual metadata")
        ontologies = {
            'horizon_classification': SampleHorizonClassification,
            'soil_sample_storage_method': SampleStorageMethod,
            'broad_land_use': SampleLandUse,
            'detailed_land_use': SampleLandUse,
            'general_ecological_zone': SampleEcologicalZone,
            'vegetation_type': SampleVegetationType,
            'profile_position': SampleProfilePosition,
            'australian_soil_classification': SampleAustralianSoilClassification,
            'fao_soil_classification': SampleFAOSoilClassification,
            'immediate_previous_land_use': SampleLandUse,
            'tillage': SampleTillage,
            'color': SampleColor,
        }

        def _make_context():
            for row in rows:
                bpa_id = row['bpa_id']
                if bpa_id is None:
                    continue
                attrs = {
                    'id': int(bpa_id.split('.')[-1])
                }
                for field in ontologies:
                    if field not in row:
                        continue
                    attrs[field + '_id'] = mappings[field][row[field]]
                for field, value in row.items():
                    if field in attrs or (field + '_id') in attrs or field == 'bpa_id':
                        continue
                    attrs[field] = value
                yield SampleContext(**attrs)

        rows = [t._asdict() for t in contextual_rows(glob(self._import_base + '/contextual-*.xlsx')[0])]
        mappings = self._load_ontology(ontologies, rows)
        self._session.bulk_save_objects(_make_context())
        self._session.commit()

    def load_otu(self):
        otu_lookup = dict(self._session.query(OTU.code, OTU.id))

        def _missing_bpa_ids(fname):
            have_bpaids = set([t[0] for t in self._session.query(SampleContext.id)])
            with open(fname, 'r') as fd:
                reader = csv.reader(fd, dialect='excel-tab')
                header = next(reader)
                bpa_ids = [int(t.split('/')[-1]) for t in header[1:]]
                for bpa_id in bpa_ids:
                    if bpa_id not in have_bpaids:
                        yield bpa_id

        def _make_otus(fname):
            # note: (for now) we have to cope with duplicate columns in the input files.
            # we just make sure they don't clash, and this can be reported to CSIRO
            with open(fname, 'r') as fd:
                reader = csv.reader(fd, dialect='excel-tab')
                header = next(reader)
                bpa_ids = [int(t.split('/')[-1]) for t in header[1:]]
                for row in reader:
                    otu_id = otu_lookup[row[0]]
                    to_make = {}
                    for bpa_id, count in zip(bpa_ids, row[1:]):
                        if count == '' or count == '0' or count == '0.0':
                            continue
                        count = int(float(count))
                        if bpa_id in to_make and to_make[bpa_id] != count:
                            raise Exception("conflicting OTU data, abort.")
                        to_make[bpa_id] = count
                    for bpa_id, count in to_make.items():
                        yield SampleOTU(sample_id=bpa_id, otu_id=otu_id, count=int(count))

        missing_bpa_ids = set()
        for fname in glob(self._import_base + '/*.txt'):
            logger.warning("first pass, reading from: %s" % (fname))
            missing_bpa_ids |= set(_missing_bpa_ids(fname))
        logger.warning("creating empty context for BPA IDs: %s" % (missing_bpa_ids))
        self._session.bulk_save_objects(SampleContext(id=t) for t in missing_bpa_ids)
        self._session.commit()

        commit_size = 100000
        for fname in glob(self._import_base + '/*.txt'):
            logger.warning("second pass, reading from: %s" % (fname))
            for commit_block in grouper(_make_otus(fname), commit_size):
                logger.warning("commiting block of ~ %d objects" % (commit_size))
                self._session.bulk_save_objects(filter(None, commit_block))
                self._session.commit()