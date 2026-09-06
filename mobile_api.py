# Mobile API for iOS & Android Apps
# RESTful API with comprehensive endpoints

from flask import Blueprint, request, jsonify, send_file
from functools import wraps
import logging
import json
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

mobile_api = Blueprint('mobile_api', __name__, url_prefix='/api/mobile/v1')


def require_api_key(f):
    """Decorator to check API key"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        # In production, validate against database
        if not api_key:
            return jsonify({'error': 'API key required'}), 401
        return f(*args, **kwargs)
    return decorated_function


@mobile_api.route('/auth/register', methods=['POST'])
def register():
    """
    Register a new mobile app user
    """
    try:
        data = request.json
        email = data.get('email')
        username = data.get('username')
        
        if not email or not username:
            return jsonify({'error': 'Email and username required'}), 400
        
        # Generate API key
        import uuid
        api_key = str(uuid.uuid4())
        
        # In production, save to database
        return jsonify({
            'success': True,
            'api_key': api_key,
            'user': {
                'username': username,
                'email': email,
                'created_at': datetime.now().isoformat()
            }
        }), 201
    
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({'error': 'Registration failed'}), 500


@mobile_api.route('/generate/quick', methods=['POST'])
@require_api_key
def generate_quick():
    """
    Quick video generation endpoint for mobile apps
    Returns: job_id immediately
    """
    try:
        data = request.json
        prompt = data.get('prompt')
        tool = data.get('tool', 'ltx_video')
        
        if not prompt:
            return jsonify({'error': 'Prompt required'}), 400
        
        # Create job
        import uuid
        job_id = str(uuid.uuid4())
        
        # In production, add to queue and return immediately
        return jsonify({
            'success': True,
            'job_id': job_id,
            'tool': tool,
            'prompt': prompt,
            'status': 'queued',
            'estimated_time': 60  # seconds
        }), 202
    
    except Exception as e:
        logger.error(f"Quick generation error: {str(e)}")
        return jsonify({'error': 'Generation failed'}), 500


@mobile_api.route('/generate/advanced', methods=['POST'])
@require_api_key
def generate_advanced():
    """
    Advanced video generation with all options
    """
    try:
        data = request.json
        
        prompt = data.get('prompt')
        tool = data.get('tool', 'ltx_video')
        resolution = data.get('resolution', '768x576')
        duration = data.get('duration', 4)
        style = data.get('style')  # Custom style
        seed = data.get('seed', -1)
        effects = data.get('effects', [])  # List of effects to apply
        
        if not prompt:
            return jsonify({'error': 'Prompt required'}), 400
        
        import uuid
        job_id = str(uuid.uuid4())
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'options': {
                'tool': tool,
                'prompt': prompt,
                'resolution': resolution,
                'duration': duration,
                'style': style,
                'seed': seed,
                'effects': effects
            },
            'status': 'queued',
            'estimated_time': 120
        }), 202
    
    except Exception as e:
        logger.error(f"Advanced generation error: {str(e)}")
        return jsonify({'error': 'Generation failed'}), 500


@mobile_api.route('/job/<job_id>', methods=['GET'])
@require_api_key
def get_job(job_id):
    """
    Get job status and details
    """
    try:
        # In production, fetch from database
        return jsonify({
            'job_id': job_id,
            'status': 'processing',  # pending, processing, completed, failed
            'progress': 45,  # 0-100
            'tool': 'ltx_video',
            'prompt': 'A beautiful sunset',
            'created_at': datetime.now().isoformat(),
            'estimated_completion': (datetime.now() + timedelta(seconds=30)).isoformat(),
            'video_url': None  # URL when complete
        }), 200
    
    except Exception as e:
        logger.error(f"Error getting job: {str(e)}")
        return jsonify({'error': 'Failed to get job'}), 500


@mobile_api.route('/job/<job_id>/stream', methods=['GET'])
@require_api_key
def stream_job_status(job_id):
    """
    Server-Sent Events (SSE) stream for real-time job updates
    """
    def event_stream():
        # Stream job progress in real-time
        for i in range(0, 101, 10):
            data = {
                'job_id': job_id,
                'progress': i,
                'status': 'processing' if i < 100 else 'completed'
            }
            yield f"data: {json.dumps(data)}\n\n"
            import time
            time.sleep(1)
    
    return event_stream(), 200, {'Content-Type': 'text/event-stream'}


@mobile_api.route('/download/<job_id>', methods=['GET'])
@require_api_key
def download_video(job_id):
    """
    Download generated video
    """
    try:
        # In production, fetch video from storage
        video_path = f"outputs/video_{job_id}.mp4"
        
        return send_file(
            video_path,
            mimetype='video/mp4',
            as_attachment=True,
            download_name=f'video_{job_id}.mp4'
        )
    
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        return jsonify({'error': 'Failed to download video'}), 500


@mobile_api.route('/tools', methods=['GET'])
def get_tools():
    """
    List all available tools with details for mobile app
    """
    tools = {
        'ltx_video': {
            'id': 'ltx_video',
            'name': 'LTX-Video',
            'description': 'Fastest AI video generator',
            'type': 'text-to-video',
            'speed': 5,  # 1-5 rating
            'quality': 3,
            'vram_required': '8GB',
            'estimated_time': 30,  # seconds
            'supports_effects': True,
            'supports_styles': False,
            'max_duration': 30
        },
        'wan_22': {
            'id': 'wan_22',
            'name': 'Wan 2.2',
            'description': 'Best quality AI video',
            'type': 'text-to-video',
            'speed': 2,
            'quality': 5,
            'vram_required': '12GB',
            'estimated_time': 120,
            'supports_effects': True,
            'supports_styles': True,
            'max_duration': 30
        }
        # ... add other tools
    }
    
    return jsonify(tools), 200


@mobile_api.route('/queue', methods=['GET'])
@require_api_key
def get_queue():
    """
    Get user's job queue
    """
    try:
        # In production, fetch from database
        jobs = [
            {
                'job_id': 'job1',
                'status': 'completed',
                'progress': 100,
                'prompt': 'Beautiful sunset'
            },
            {
                'job_id': 'job2',
                'status': 'processing',
                'progress': 45,
                'prompt': 'Cat walking in garden'
            }
        ]
        
        return jsonify({
            'total': len(jobs),
            'completed': sum(1 for j in jobs if j['status'] == 'completed'),
            'processing': sum(1 for j in jobs if j['status'] == 'processing'),
            'jobs': jobs
        }), 200
    
    except Exception as e:
        logger.error(f"Error getting queue: {str(e)}")
        return jsonify({'error': 'Failed to get queue'}), 500


@mobile_api.route('/history', methods=['GET'])
@require_api_key
def get_history():
    """
    Get user's generation history
    """
    try:
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # In production, fetch from database
        history = []
        
        return jsonify({
            'total': len(history),
            'limit': limit,
            'offset': offset,
            'history': history
        }), 200
    
    except Exception as e:
        logger.error(f"Error getting history: {str(e)}")
        return jsonify({'error': 'Failed to get history'}), 500


@mobile_api.route('/usage', methods=['GET'])
@require_api_key
def get_usage():
    """
    Get user's API usage statistics
    """
    try:
        # In production, fetch from database
        usage = {
            'total_videos': 42,
            'total_duration': 168,  # seconds
            'this_month': 12,
            'quota': 100,
            'quota_remaining': 58,
            'last_reset': (datetime.now() - timedelta(days=15)).isoformat(),
            'next_reset': (datetime.now() + timedelta(days=15)).isoformat()
        }
        
        return jsonify(usage), 200
    
    except Exception as e:
        logger.error(f"Error getting usage: {str(e)}")
        return jsonify({'error': 'Failed to get usage'}), 500


@mobile_api.route('/effects', methods=['GET'])
def get_effects():
    """
    Get available video effects
    """
    effects = {
        'fade': {
            'id': 'fade',
            'name': 'Fade In/Out',
            'description': 'Add fade in and fade out effects',
            'duration': 1,  # seconds
            'params': ['duration']
        },
        'watermark': {
            'id': 'watermark',
            'name': 'Watermark',
            'description': 'Add watermark text',
            'params': ['text', 'position', 'opacity']
        },
        'speedup': {
            'id': 'speedup',
            'name': 'Speed Up',
            'description': 'Speed up playback',
            'params': ['factor']
        }
    }
    
    return jsonify(effects), 200


@mobile_api.route('/health', methods=['GET'])
def health():
    """
    API health check
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }), 200


@mobile_api.route('/docs', methods=['GET'])
def api_docs():
    """
    API documentation
    """
    docs = """
    # AI Video Generator Mobile API
    
    ## Authentication
    All endpoints require X-API-Key header
    
    ## Endpoints
    
    ### POST /api/mobile/v1/auth/register
    Register new user and get API key
    
    ### POST /api/mobile/v1/generate/quick
    Quick video generation (LTX-Video)
    
    ### POST /api/mobile/v1/generate/advanced
    Advanced generation with all options
    
    ### GET /api/mobile/v1/job/{job_id}
    Get job status
    
    ### GET /api/mobile/v1/job/{job_id}/stream
    Stream real-time job updates (SSE)
    
    ### GET /api/mobile/v1/download/{job_id}
    Download generated video
    
    ### GET /api/mobile/v1/tools
    List available tools
    
    ### GET /api/mobile/v1/effects
    List available effects
    """
    
    return docs, 200, {'Content-Type': 'text/plain'}
