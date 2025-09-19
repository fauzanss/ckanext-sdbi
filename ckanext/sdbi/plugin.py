from collections import OrderedDict
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.common import config
import ckan.model as model

def most_recent_datasets(num=4):
        datasets = toolkit.get_action('package_search')({}, {'sort': 'metadata_modified desc',
                                                        'fq': 'private:false',
                                                        'rows': num})
        return datasets.get('results', [])

def most_popular_datasets(num=4):
    """Get most popular datasets based on view count using direct SQL JOIN"""
    try:
        from sqlalchemy import text
        
        # Use direct SQL query with JOIN to get datasets ordered by view count
        query = text("""
            SELECT p.id, p.name, p.title, p.notes, p.state, p.private, 
                   p.metadata_created, p.metadata_modified,
                   COUNT(t.url) as view_count
            FROM package p
            LEFT JOIN tracking_raw t ON t.url = '/dataset/' || p.name
            WHERE p.state = 'active' AND p.private = false
            GROUP BY p.id, p.name, p.title, p.notes, p.state, p.private, 
                     p.metadata_created, p.metadata_modified
            ORDER BY view_count DESC, p.metadata_modified DESC
            LIMIT :limit
        """)
        
        result = model.Session.execute(query, {'limit': num})
        
        # Get package IDs from SQL result
        package_ids = [row.id for row in result]
        
        if not package_ids:
            return []
        
        # Get full package data using CKAN API for proper formatting
        packages = []
        for package_id in package_ids:
            try:
                package = toolkit.get_action('package_show')({}, {'id': package_id})
                packages.append(package)
            except:
                continue
        
        return packages
        
    except Exception as e:
        # Fallback to recent datasets if there's an error
        return most_recent_datasets(num)

def dataset_count():
    """Return a count of all datasets"""
    try:
        from sqlalchemy import text
        
        query = text("""
            SELECT COUNT(*) as total
            FROM package 
            WHERE state = 'active' AND private = false
        """)
        
        result = model.Session.execute(query)
        row = result.fetchone()
        return row.total if row else 0
        
    except Exception as e:
        # Fallback to original method
        result = toolkit.get_action('package_search')({}, {'rows': 1})
        return result['count']

def get_connected_statistics():
    """Get statistics for connected provinces, NGOs, and ministries/institutions using dynamic table-based approach"""
    try:
        from sqlalchemy import text
        
        # Use dynamic table-based approach for better maintainability
        query = text("""
            WITH dataset_text AS (
                SELECT 
                    name,
                    title,
                    notes,
                    LOWER(CONCAT(title, ' ', COALESCE(notes, ''))) as full_text
                FROM package 
                WHERE state = 'active' AND private = false
            ),
            provinsi_matches AS (
                SELECT DISTINCT pk.provinsi_name
                FROM dataset_text dt
                JOIN provinsi_keywords pk ON dt.full_text LIKE '%' || pk.keyword || '%'
            ),
            kabupaten_kota_matches AS (
                SELECT DISTINCT kkk.kabupaten_kota_name
                FROM dataset_text dt
                JOIN kabupaten_kota_keywords kkk ON dt.full_text LIKE '%' || kkk.keyword || '%'
            ),
            kementerian_matches AS (
                SELECT DISTINCT kk.kementerian_name
                FROM dataset_text dt
                JOIN kementerian_keywords kk ON dt.full_text LIKE '%' || kk.keyword || '%'
            )
            SELECT 
                (SELECT COUNT(*) FROM provinsi_matches) as provinsi_count,
                (SELECT COUNT(*) FROM kabupaten_kota_matches) as kabupaten_kota_count,
                (SELECT COUNT(*) FROM kementerian_matches) as kementerian_count
        """)
        
        result = model.Session.execute(query)
        row = result.fetchone()
        
        return {
            'provinsi_terhubung': row.provinsi_count if row else 0,
            'kabupaten_kota_terhubung': row.kabupaten_kota_count if row else 0,
            'kementerian_lembaga_terhubung': row.kementerian_count if row else 0
        }
        
    except Exception as e:
        return {
            'provinsi_terhubung': 0,
            'kabupaten_kota_terhubung': 0,
            'kementerian_lembaga_terhubung': 0
        }

def debug_connected_statistics():
    """Debug function to see all datasets and their matching using table-based approach"""
    try:
        from sqlalchemy import text
        
        # Get all datasets with their keyword matches using table-based approach
        query = text("""
            WITH dataset_text AS (
                SELECT 
                    p.name,
                    p.title,
                    p.notes,
                    LOWER(CONCAT(p.title, ' ', COALESCE(p.notes, ''))) as full_text
                FROM package p
                WHERE p.state = 'active' AND p.private = false
                ORDER BY p.metadata_created DESC
            ),
            dataset_matches AS (
                SELECT 
                    dt.name,
                    dt.title,
                    dt.notes,
                    dt.full_text,
                    -- Provinsi matches
                    STRING_AGG(DISTINCT pk.provinsi_name, ', ') as provinsi_matches,
                    STRING_AGG(DISTINCT pk.keyword, ', ') as provinsi_keywords,
                    -- Kabupaten/Kota matches
                    STRING_AGG(DISTINCT kkk.kabupaten_kota_name, ', ') as kabupaten_kota_matches,
                    STRING_AGG(DISTINCT kkk.keyword, ', ') as kabupaten_kota_keywords,
                    -- Kementerian matches
                    STRING_AGG(DISTINCT kk.kementerian_name, ', ') as kementerian_matches,
                    STRING_AGG(DISTINCT kk.keyword, ', ') as kementerian_keywords
                FROM dataset_text dt
                LEFT JOIN provinsi_keywords pk ON dt.full_text LIKE '%' || pk.keyword || '%'
                LEFT JOIN kabupaten_kota_keywords kkk ON dt.full_text LIKE '%' || kkk.keyword || '%'
                LEFT JOIN kementerian_keywords kk ON dt.full_text LIKE '%' || kk.keyword || '%'
                GROUP BY dt.name, dt.title, dt.notes, dt.full_text
            )
            SELECT 
                name,
                title,
                notes,
                full_text,
                COALESCE(provinsi_matches, '') as provinsi_matches,
                COALESCE(provinsi_keywords, '') as provinsi_keywords,
                COALESCE(kabupaten_kota_matches, '') as kabupaten_kota_matches,
                COALESCE(kabupaten_kota_keywords, '') as kabupaten_kota_keywords,
                COALESCE(kementerian_matches, '') as kementerian_matches,
                COALESCE(kementerian_keywords, '') as kementerian_keywords
            FROM dataset_matches
            ORDER BY name
        """)
        
        result = model.Session.execute(query)
        datasets = []
        
        for row in result:
            datasets.append({
                'name': row.name,
                'title': row.title,
                'notes': row.notes or '',
                'full_text': row.full_text[:200] + '...' if len(row.full_text) > 200 else row.full_text,
                'provinsi_matches': row.provinsi_matches.split(', ') if row.provinsi_matches else [],
                'provinsi_keywords': row.provinsi_keywords.split(', ') if row.provinsi_keywords else [],
                'kabupaten_kota_matches': row.kabupaten_kota_matches.split(', ') if row.kabupaten_kota_matches else [],
                'kabupaten_kota_keywords': row.kabupaten_kota_keywords.split(', ') if row.kabupaten_kota_keywords else [],
                'kementerian_matches': row.kementerian_matches.split(', ') if row.kementerian_matches else [],
                'kementerian_keywords': row.kementerian_keywords.split(', ') if row.kementerian_keywords else []
            })
        
        # Get all available keywords from tables
        provinsi_query = text("SELECT DISTINCT provinsi_name, keyword FROM provinsi_keywords ORDER BY provinsi_name, keyword")
        kabupaten_kota_query = text("SELECT DISTINCT kabupaten_kota_name, keyword FROM kabupaten_kota_keywords ORDER BY kabupaten_kota_name, keyword")
        kementerian_query = text("SELECT DISTINCT kementerian_name, keyword FROM kementerian_keywords ORDER BY kementerian_name, keyword")
        
        provinsi_result = model.Session.execute(provinsi_query)
        kabupaten_kota_result = model.Session.execute(kabupaten_kota_query)
        kementerian_result = model.Session.execute(kementerian_query)
        
        all_keywords = {
            'provinsi': [{'name': row.provinsi_name, 'keyword': row.keyword} for row in provinsi_result],
            'kabupaten_kota': [{'name': row.kabupaten_kota_name, 'keyword': row.keyword} for row in kabupaten_kota_result],
            'kementerian': [{'name': row.kementerian_name, 'keyword': row.keyword} for row in kementerian_result]
        }
        
        return {
            'datasets': datasets,
            'keywords': all_keywords,
            'total_datasets': len(datasets),
            'matched_datasets': len([d for d in datasets if any([d['provinsi_matches'], d['kabupaten_kota_matches'], d['kementerian_matches']])])
        }
        
    except Exception as e:
        return {
            'datasets': [],
            'keywords': {
                'provinsi': [],
                'kabupaten_kota': [],
                'kementerian': []
            },
            'total_datasets': 0,
            'matched_datasets': 0,
            'error': str(e)
        }

def groups():
    """Return a list of groups"""

    return toolkit.get_action('group_list')({}, {'all_fields': True})

def package_showcase_list(context):
    return toolkit.get_action('ckanext_package_showcase_list')({}, {'package_id': context.pkg_dict['id']})

def ckan_site_url():
    return config.get('ckan.site_url', '').rstrip('/')

def get_dataset_views(package_id):
    """Get tracking data for a dataset directly from raw tracking table"""
    try:
        # Get dataset name from package_id
        package = model.Package.get(package_id)
        if not package:
            return {'total_views': 0, 'recent_views': 0}
        
        dataset_url = f"/dataset/{package.name}"
        
        # Get total views from raw tracking table
        total_views = model.Session.query(model.TrackingRaw).filter(
            model.TrackingRaw.url == dataset_url
        ).count()
        
        # Get recent views (last 7 days)
        from datetime import datetime, timedelta
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        
        recent_views = model.Session.query(model.TrackingRaw).filter(
            model.TrackingRaw.url == dataset_url,
            model.TrackingRaw.access_timestamp >= seven_days_ago
        ).count()
        
        # Get today's views
        today = datetime.utcnow().date()
        today_views = model.Session.query(model.TrackingRaw).filter(
            model.TrackingRaw.url == dataset_url,
            model.Session.func.date(model.TrackingRaw.access_timestamp) == today
        ).count()
        
        return {
            'total_views': total_views,
            'recent_views': recent_views,
            'today_views': today_views
        }
    except Exception as e:
        # Fallback to CKAN's tracking system if direct query fails
        try:
            tracking_summary = model.TrackingSummary.get_for_package(package_id)
            if tracking_summary:
                return {
                    'total_views': tracking_summary.get('total', 0),
                    'recent_views': tracking_summary.get('recent', 0),
                    'today_views': 0
                }
        except:
            pass
        return {'total_views': 0, 'recent_views': 0, 'today_views': 0}

def get_dataset_views_by_name(dataset_name):
    """Get tracking data for a dataset by name"""
    try:
        dataset_url = f"/dataset/{dataset_name}"
        
        # Use direct SQL query for better reliability
        from sqlalchemy import text
        
        # Get total views
        result = model.Session.execute(text("""
            SELECT COUNT(*) as count FROM tracking_raw 
            WHERE url = :url
        """), {'url': dataset_url})
        total_views = result.fetchone()[0]
        
        # Get recent views (last 7 days)
        from datetime import datetime, timedelta
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        
        result = model.Session.execute(text("""
            SELECT COUNT(*) as count FROM tracking_raw 
            WHERE url = :url AND access_timestamp >= :seven_days_ago
        """), {'url': dataset_url, 'seven_days_ago': seven_days_ago})
        recent_views = result.fetchone()[0]
        
        # Get today's views
        today = datetime.utcnow().date()
        result = model.Session.execute(text("""
            SELECT COUNT(*) as count FROM tracking_raw 
            WHERE url = :url AND DATE(access_timestamp) = :today
        """), {'url': dataset_url, 'today': today})
        today_views = result.fetchone()[0]
        
        return {
            'total_views': total_views,
            'recent_views': recent_views,
            'today_views': today_views
        }
    except Exception as e:
        # Return fallback data
        return {'total_views': 0, 'recent_views': 0, 'today_views': 0}

def get_dataset_downloads(package_id):
    """Get download count for a dataset from resource tracking data"""
    try:
        # Get dataset name from package_id
        package = model.Package.get(package_id)
        if not package:
            return {'total_downloads': 0, 'recent_downloads': 0}
        
        dataset_url = f"/dataset/{package.name}"
        
        # Get all resources for this dataset
        resources = package.resources
        
        # Count downloads for all resources of this dataset
        from sqlalchemy import text
        from datetime import datetime, timedelta
        
        # Get total downloads
        result = model.Session.execute(text("""
            SELECT COUNT(*) as count FROM tracking_raw 
            WHERE tracking_type = 'resource' 
            AND url LIKE :dataset_pattern
        """), {'dataset_pattern': f"{dataset_url}/resource/%"})
        total_downloads = result.fetchone()[0]
        
        # Get recent downloads (last 7 days)
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        result = model.Session.execute(text("""
            SELECT COUNT(*) as count FROM tracking_raw 
            WHERE tracking_type = 'resource' 
            AND url LIKE :dataset_pattern
            AND access_timestamp >= :seven_days_ago
        """), {
            'dataset_pattern': f"{dataset_url}/resource/%",
            'seven_days_ago': seven_days_ago
        })
        recent_downloads = result.fetchone()[0]
        
        # Get today's downloads
        today = datetime.utcnow().date()
        result = model.Session.execute(text("""
            SELECT COUNT(*) as count FROM tracking_raw 
            WHERE tracking_type = 'resource' 
            AND url LIKE :dataset_pattern
            AND DATE(access_timestamp) = :today
        """), {
            'dataset_pattern': f"{dataset_url}/resource/%",
            'today': today
        })
        today_downloads = result.fetchone()[0]
        
        return {
            'total_downloads': total_downloads,
            'recent_downloads': recent_downloads,
            'today_downloads': today_downloads
        }
    except Exception as e:
        return {'total_downloads': 0, 'recent_downloads': 0, 'today_downloads': 0}

def get_dataset_downloads_by_name(dataset_name):
    """Get download count for a dataset by name"""
    try:
        # Use direct SQL query for better reliability
        from sqlalchemy import text
        from datetime import datetime, timedelta
        
        # Get dataset ID from name first
        result = model.Session.execute(text("""
            SELECT id FROM package WHERE name = :dataset_name
        """), {'dataset_name': dataset_name})
        dataset_row = result.fetchone()
        
        if not dataset_row:
            return {'total_downloads': 0, 'recent_downloads': 0, 'today_downloads': 0}
        
        dataset_id = dataset_row[0]
        
        # Get total downloads - menggunakan dataset ID
        result = model.Session.execute(text("""
            SELECT COUNT(*) as count FROM tracking_raw 
            WHERE tracking_type = 'resource' 
            AND url LIKE :dataset_pattern
        """), {'dataset_pattern': f"%/dataset/{dataset_id}/resource/%"})
        total_downloads = result.fetchone()[0]
        
        # Get recent downloads (last 7 days)
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        result = model.Session.execute(text("""
            SELECT COUNT(*) as count FROM tracking_raw 
            WHERE tracking_type = 'resource' 
            AND url LIKE :dataset_pattern
            AND access_timestamp >= :seven_days_ago
        """), {
            'dataset_pattern': f"%/dataset/{dataset_id}/resource/%",
            'seven_days_ago': seven_days_ago
        })
        recent_downloads = result.fetchone()[0]
        
        # Get today's downloads
        today = datetime.utcnow().date()
        result = model.Session.execute(text("""
            SELECT COUNT(*) as count FROM tracking_raw 
            WHERE tracking_type = 'resource' 
            AND url LIKE :dataset_pattern
            AND DATE(access_timestamp) = :today
        """), {
            'dataset_pattern': f"%/dataset/{dataset_id}/resource/%",
            'today': today
        })
        today_downloads = result.fetchone()[0]
        
        return {
            'total_downloads': total_downloads,
            'recent_downloads': recent_downloads,
            'today_downloads': today_downloads
        }
    except Exception as e:
        return {'total_downloads': 0, 'recent_downloads': 0, 'today_downloads': 0}

def get_total_visitors():
    """Get total number of unique visitors from tracking_raw table"""
    try:
        from sqlalchemy import text
        
        # Get total unique visitors (unique user_key)
        result = model.Session.execute(text("""
            SELECT COUNT(DISTINCT user_key) as count FROM tracking_raw 
            WHERE user_key != 'anonymous'
        """))
        unique_visitors = result.fetchone()[0]
        
        # Get total page views
        result = model.Session.execute(text("""
            SELECT COUNT(*) as count FROM tracking_raw
        """))
        total_views = result.fetchone()[0]
        
        # Get today's visitors
        from datetime import datetime, timedelta
        today = datetime.utcnow().date()
        
        result = model.Session.execute(text("""
            SELECT COUNT(DISTINCT user_key) as count FROM tracking_raw 
            WHERE DATE(access_timestamp) = :today AND user_key != 'anonymous'
        """), {'today': today})
        today_visitors = result.fetchone()[0]
        
        # Get yesterday's visitors
        yesterday = today - timedelta(days=1)
        result = model.Session.execute(text("""
            SELECT COUNT(DISTINCT user_key) as count FROM tracking_raw 
            WHERE DATE(access_timestamp) = :yesterday AND user_key != 'anonymous'
        """), {'yesterday': yesterday})
        yesterday_visitors = result.fetchone()[0]
        
        # Get online visitors (active in last 5 minutes)
        five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)
        result = model.Session.execute(text("""
            SELECT COUNT(DISTINCT user_key) as count FROM tracking_raw 
            WHERE access_timestamp >= :five_minutes_ago AND user_key != 'anonymous'
        """), {'five_minutes_ago': five_minutes_ago})
        online_visitors = result.fetchone()[0]
        
        return {
            'unique_visitors': unique_visitors,
            'total_views': total_views,
            'today_visitors': today_visitors,
            'yesterday_visitors': yesterday_visitors,
            'online_visitors': online_visitors
        }
    except Exception as e:
        return {
            'unique_visitors': 0,
            'total_views': 0,
            'today_visitors': 0,
            'yesterday_visitors': 0,
            'online_visitors': 0
        }

def json_loads(data):
    """Parse JSON string safely"""
    try:
        import json
        if data:
            return json.loads(data)
        return None
    except (ValueError, TypeError):
        return None

class SDBIPlugin(plugins.SingletonPlugin):
    # SDBI Plugin for BNPB Data Portal
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IFacets, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IBlueprint)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'sdbi')

    # IFacets
    def dataset_facets(self, facets_dict, package_type):

        if package_type != 'dataset':
            return facets_dict

        return OrderedDict([('jenis', 'Jenis Bencana'),
                            ('fase', 'Fase'),
                            #('groups', 'Grup'),
                            ('organization', 'Organisasi'),
                            #('vocab_category_all', 'Topic Categories'),
                            #('metadata_type', 'Dataset Type'),
                            #('tags', 'Tagging'),
                            ('res_format', 'Format'),
                            #('organization_type', 'Organization Types'),
                            #('publisher', 'Publishers'),
                            #('extras_progress', 'Progress'),
                            ])

    def organization_facets(self, facets_dict, organization_type, package_type):

        if not package_type:
            return OrderedDict([('organization', 'Organisasi'),
                                ('jenis', 'Jenis Bencana'),
                                ('fase', 'Fase'),
                                #('groups', 'Grup'),
                                #('organization', 'Instansi'),
                                #('vocab_category_all', 'Topic Categories'),
                                #('metadata_type', 'Dataset Type'),
                                #('tags', 'Tagging'),
                                ('res_format', 'Format'),
                                #('harvest_source_title', 'Harvest Source'),
                                #('capacity', 'Visibility'),
                                #('dataset_type', 'Resource Type'),
                                #('publisher', 'Publishers'),
                                ])
        else:
            return facets_dict

    def group_facets(self, facets_dict, group_type, package_type):

        # get the categories key
        group_id = plugins.toolkit.c.group_dict['id']
        key = 'vocab___category_tag_%s' % group_id
        if not package_type:
            return OrderedDict([('jenis', 'Jenis Bencana'),
                                ('fase', 'Fase'),
                                #('groups', 'Grup'),
                                ('organization', 'Organisasi'),
                                #('metadata_type', 'Dataset Type'),
                                #('organization_type', 'Organization Types'),
                                #('tags', 'Tagging'),
                                ('res_format', 'Format'),
                                #(key, 'Categories'),
                                #('publisher', 'Publisher'),
                                ])
        else:
            return facets_dict

    def get_helpers(self):
        """Register sdbi_theme_* helper functions"""

        return {'sdbi_theme_most_recent_datasets': most_recent_datasets,
                'sdbi_theme_most_popular_datasets': most_popular_datasets,
                'sdbi_theme_dataset_count': dataset_count,
                'sdbi_theme_connected_statistics': get_connected_statistics,
                'sdbi_theme_debug_connected': debug_connected_statistics,
                'sdbi_theme_groups': groups,
                'ckan_site_url': ckan_site_url,
                'package_showcase_list': package_showcase_list,
                'get_dataset_views': get_dataset_views,
                'get_dataset_views_by_name': get_dataset_views_by_name,
                'get_dataset_downloads': get_dataset_downloads,
                'get_dataset_downloads_by_name': get_dataset_downloads_by_name,
                'get_total_visitors': get_total_visitors,
                'json_loads': json_loads}

    # IBlueprint
    def get_blueprint(self):
        """Register blueprints"""
        import logging
        log = logging.getLogger(__name__)
        log.info("Registering blueprints")
        
        from ckanext.sdbi.controllers.google_forms import google_forms_blueprint
        from ckanext.sdbi.controllers.tracking import TrackingController
        
        # Create tracking blueprint
        from flask import Blueprint
        tracking_blueprint = Blueprint('tracking', __name__)
        
        # Add routes
        tracking_blueprint.add_url_rule('/sdbi/tracking', 'track', TrackingController().track, methods=['POST'])
        tracking_blueprint.add_url_rule('/sdbi/tracking/page', 'track_page', TrackingController().track_page, methods=['GET'])
        tracking_blueprint.add_url_rule('/sdbi/downloads/<dataset_name>', 'get_downloads', TrackingController().get_downloads, methods=['GET'])
        
        # Return list of blueprints
        return [google_forms_blueprint, tracking_blueprint]


