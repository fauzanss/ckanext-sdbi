import logging
import json
from datetime import datetime
from ckan import model
from ckan.plugins import toolkit
from flask import request
from flask import make_response as response
from ckan.common import _

log = logging.getLogger(__name__)

class TrackingController:
    """
    Custom tracking controller untuk CKAN SDBI
    Menangani tracking requests dan menyimpan ke database
    """
    
    def track(self):
        """Handle tracking requests"""
        try:
            # Get request data
            data = request.get_json() if request.is_json else request.form
            
            url = data.get('url', '')
            tracking_type = data.get('type', 'page')
            
            if not url:
                resp = response(json.dumps({'error': 'URL is required'}))
                resp.status_code = 400
                return resp
            
            # Log tracking request
            log.info(f"Tracking request: {url} ({tracking_type})")
            
            # Insert into tracking_raw table
            from ckan.model.tracking import TrackingRaw
            
            tracking_raw = TrackingRaw(
                url=url,
                tracking_type=tracking_type,
                access_timestamp=datetime.utcnow()
            )
            
            model.Session.add(tracking_raw)
            model.Session.commit()
            
            log.info(f"Tracking data saved: {url}")
            
            # Return success response
            resp = response(json.dumps({
                'success': True,
                'message': 'Tracking data saved',
                'url': url,
                'type': tracking_type,
                'timestamp': datetime.utcnow().isoformat()
            }))
            resp.status_code = 200
            return resp
            
        except Exception as e:
            log.error(f"Tracking error: {str(e)}")
            resp = response(json.dumps({'error': str(e)}))
            resp.status_code = 500
            return resp
    
    def track_page(self):
        """Track page view with GET request"""
        try:
            url = request.params.get('url', '')
            tracking_type = request.params.get('type', 'page')
            
            if not url:
                resp = response(json.dumps({'error': 'URL is required'}))
                resp.status_code = 400
                return resp
            
            # Log tracking request
            log.info(f"Page tracking: {url} ({tracking_type})")
            
            # Insert into tracking_raw table
            from ckan.model.tracking import TrackingRaw
            
            tracking_raw = TrackingRaw(
                url=url,
                tracking_type=tracking_type,
                access_timestamp=datetime.utcnow()
            )
            
            model.Session.add(tracking_raw)
            model.Session.commit()
            
            log.info(f"Page tracking saved: {url}")
            
            # Return success response
            resp = response(json.dumps({
                'success': True,
                'message': 'Page tracking saved',
                'url': url,
                'type': tracking_type,
                'timestamp': datetime.utcnow().isoformat()
            }))
            resp.status_code = 200
            return resp
            
        except Exception as e:
            log.error(f"Page tracking error: {str(e)}")
            resp = response(json.dumps({'error': str(e)}))
            resp.status_code = 500
            return resp
    
    def get_downloads(self, dataset_name):
        """Get download count for a dataset"""
        try:
            from ckanext.sdbi.plugin import get_dataset_downloads_by_name
            
            download_stats = get_dataset_downloads_by_name(dataset_name)
            
            resp = response(json.dumps(download_stats))
            resp.status_code = 200
            return resp
            
        except Exception as e:
            log.error(f"Get downloads error: {str(e)}")
            resp = response(json.dumps({'error': str(e)}))
            resp.status_code = 500
            return resp 