# Batch Processing Module
# Generate multiple videos from a CSV or text file

import csv
import json
import os
from pathlib import Path
from datetime import datetime
import threading
import logging

logger = logging.getLogger(__name__)


class BatchProcessor:
    """
    Process multiple video generation jobs from file
    """
    
    def __init__(self, app_context):
        self.app = app_context
        self.jobs = {}
        self.batch_id = None
    
    def load_from_csv(self, file_path):
        """
        Load batch jobs from CSV file
        Format: prompt,tool,resolution,duration
        """
        try:
            jobs = []
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    jobs.append({
                        'prompt': row.get('prompt', ''),
                        'tool': row.get('tool', 'ltx_video'),
                        'resolution': row.get('resolution', '768x576'),
                        'duration': int(row.get('duration', 4))
                    })
            return jobs
        except Exception as e:
            logger.error(f"Error loading CSV: {str(e)}")
            raise
    
    def load_from_json(self, file_path):
        """
        Load batch jobs from JSON file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                return data
            else:
                return [data]
        except Exception as e:
            logger.error(f"Error loading JSON: {str(e)}")
            raise
    
    def load_from_text(self, file_path):
        """
        Load batch jobs from text file (one prompt per line)
        """
        try:
            jobs = []
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    prompt = line.strip()
                    if prompt:
                        jobs.append({
                            'prompt': prompt,
                            'tool': 'ltx_video',
                            'resolution': '768x576',
                            'duration': 4
                        })
            return jobs
        except Exception as e:
            logger.error(f"Error loading text file: {str(e)}")
            raise
    
    def start_batch(self, jobs, output_dir='outputs'):
        """
        Start processing batch of jobs
        """
        import uuid
        self.batch_id = str(uuid.uuid4())
        
        batch_info = {
            'id': self.batch_id,
            'total': len(jobs),
            'completed': 0,
            'failed': 0,
            'start_time': datetime.now().isoformat(),
            'end_time': None,
            'jobs': []
        }
        
        self.jobs[self.batch_id] = batch_info
        
        # Process in background thread
        thread = threading.Thread(
            target=self._process_batch,
            args=(self.batch_id, jobs, output_dir)
        )
        thread.daemon = True
        thread.start()
        
        return self.batch_id
    
    def _process_batch(self, batch_id, jobs, output_dir):
        """
        Process batch jobs sequentially
        """
        try:
            for i, job_spec in enumerate(jobs):
                try:
                    logger.info(f"Processing batch {batch_id}, job {i+1}/{len(jobs)}")
                    
                    # Generate video using the app's generate_video function
                    # This would be integrated with your existing app
                    
                    self.jobs[batch_id]['completed'] += 1
                    self.jobs[batch_id]['jobs'].append({
                        'index': i + 1,
                        'prompt': job_spec.get('prompt'),
                        'status': 'completed',
                        'output': f"{output_dir}/video_{batch_id}_{i+1}.mp4"
                    })
                
                except Exception as e:
                    logger.error(f"Error processing job {i+1}: {str(e)}")
                    self.jobs[batch_id]['failed'] += 1
                    self.jobs[batch_id]['jobs'].append({
                        'index': i + 1,
                        'prompt': job_spec.get('prompt'),
                        'status': 'failed',
                        'error': str(e)
                    })
            
            self.jobs[batch_id]['end_time'] = datetime.now().isoformat()
        
        except Exception as e:
            logger.error(f"Batch processing error: {str(e)}")
    
    def get_batch_status(self, batch_id):
        """
        Get status of a batch job
        """
        return self.jobs.get(batch_id, None)
    
    def list_batches(self):
        """
        List all batch jobs
        """
        return list(self.jobs.values())


class VideoEffects:
    """
    Apply effects to generated videos
    """
    
    def __init__(self):
        pass
    
    @staticmethod
    def apply_fade(input_path, output_path, duration=1):
        """
        Apply fade in/out effect
        """
        try:
            import cv2
            import numpy as np
            
            cap = cv2.VideoCapture(input_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            frame_count = 0
            fade_frames = int(fps * duration)
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Apply fade
                if frame_count < fade_frames:
                    alpha = frame_count / fade_frames
                    frame = cv2.addWeighted(frame, alpha, np.zeros_like(frame), 0, 0)
                elif frame_count > int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - fade_frames:
                    alpha = (int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - frame_count) / fade_frames
                    frame = cv2.addWeighted(frame, alpha, np.zeros_like(frame), 0, 0)
                
                out.write(frame)
                frame_count += 1
            
            cap.release()
            out.release()
            
            logger.info(f"Fade effect applied: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Error applying fade effect: {str(e)}")
            raise
    
    @staticmethod
    def add_watermark(input_path, output_path, watermark_text='Generated with AI', position='bottom-right'):
        """
        Add watermark text to video
        """
        try:
            import cv2
            
            cap = cv2.VideoCapture(input_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            # Calculate text position
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.6
            thickness = 1
            text_size = cv2.getTextSize(watermark_text, font, font_scale, thickness)[0]
            
            if position == 'bottom-right':
                text_pos = (width - text_size[0] - 10, height - 10)
            elif position == 'bottom-left':
                text_pos = (10, height - 10)
            elif position == 'top-right':
                text_pos = (width - text_size[0] - 10, 30)
            else:  # top-left
                text_pos = (10, 30)
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                cv2.putText(frame, watermark_text, text_pos, font, font_scale, (255, 255, 255), thickness)
                out.write(frame)
            
            cap.release()
            out.release()
            
            logger.info(f"Watermark added: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Error adding watermark: {str(e)}")
            raise
    
    @staticmethod
    def speed_up(input_path, output_path, speed_factor=1.5):
        """
        Speed up video playback
        """
        try:
            import cv2
            import numpy as np
            
            cap = cv2.VideoCapture(input_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            new_fps = fps * speed_factor
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, new_fps, (width, height))
            
            frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Skip frames based on speed factor
                if frame_count % int(speed_factor) == 0:
                    out.write(frame)
                
                frame_count += 1
            
            cap.release()
            out.release()
            
            logger.info(f"Video speed increased {speed_factor}x: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Error speeding up video: {str(e)}")
            raise
    
    @staticmethod
    def add_audio(input_path, audio_path, output_path):
        """
        Add audio track to video
        """
        try:
            import subprocess
            
            # Using ffmpeg for audio mixing
            cmd = [
                'ffmpeg',
                '-i', input_path,
                '-i', audio_path,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-map', '0:v:0',
                '-map', '1:a:0',
                '-y',
                output_path
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Audio added: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Error adding audio: {str(e)}")
            raise
