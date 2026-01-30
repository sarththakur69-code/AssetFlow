"""
Scan History Manager for AssetFlow
Handles saving, loading, and managing scan history using browser localStorage.
"""

import streamlit as st
import json
from datetime import datetime

class HistoryManager:
    """Manages scan history using Streamlit session state and localStorage"""
    
    @staticmethod
    def save_scan(url, url_2=None, is_battle=False):
        """
        Save current scan to history.
        
        Args:
            url: Primary URL scanned
            url_2: Secondary URL (for battle mode)
            is_battle: Boolean indicating battle mode
        """
        if 'scan_history' not in st.session_state:
            st.session_state.scan_history = []
        
        # Create scan entry
        scan_entry = {
            'timestamp': datetime.now().isoformat(),
            'url': url,
            'url_2': url_2 if is_battle else None,
            'is_battle': is_battle,
            'image_count': len(st.session_state.scraped_data) if 'scraped_data' in st.session_state and st.session_state.scraped_data else 0,
            'image_count_2': len(st.session_state.scraped_data_2) if is_battle and 'scraped_data_2' in st.session_state and st.session_state.scraped_data_2 else 0,
            'has_vibe': 'vibe' in st.session_state.get('global_stats', {}),
            # Store lightweight metadata only (not full data)
            'stats_preview': {
                'colors': st.session_state.global_stats.get('palette', [])[:5] if 'global_stats' in st.session_state else [],
                'font_count': len(st.session_state.global_stats.get('fonts', [])) if 'global_stats' in st.session_state else 0
            }
        }
        
        # Add to history (keep last 20)
        st.session_state.scan_history.insert(0, scan_entry)
        if len(st.session_state.scan_history) > 20:
            st.session_state.scan_history = st.session_state.scan_history[:20]
        
        return True
    
    @staticmethod
    def get_history():
        """Get all scan history"""
        if 'scan_history' not in st.session_state:
            st.session_state.scan_history = []
        return st.session_state.scan_history
    
    @staticmethod
    def clear_history():
        """Clear all scan history"""
        st.session_state.scan_history = []
        return True
    
    @staticmethod
    def delete_scan(index):
        """Delete specific scan from history"""
        if 'scan_history' in st.session_state and index < len(st.session_state.scan_history):
            st.session_state.scan_history.pop(index)
            return True
        return False
    
    @staticmethod
    def format_timestamp(iso_timestamp):
        """Format ISO timestamp to readable format"""
        try:
            dt = datetime.fromisoformat(iso_timestamp)
            return dt.strftime('%Y-%m-%d %H:%M')
        except:
            return iso_timestamp
    
    @staticmethod
    def display_history_sidebar():
        """Display scan history in sidebar"""
        with st.sidebar:
            st.markdown("---")
            st.subheader("SCAN HISTORY")
            
            history = HistoryManager.get_history()
            
            if not history:
                st.info("No scan history yet.")
                return
            
            # Clear all button
            if st.button("Clear All History", use_container_width=True):
                HistoryManager.clear_history()
                st.rerun()
            
            st.markdown("---")
            
            # Display history items
            for i, entry in enumerate(history):
                timestamp_formatted = HistoryManager.format_timestamp(entry['timestamp'])
                if entry['is_battle']:
                    u1 = entry['url'] or '?'
                    u2 = entry.get('url_2') or '?'
                    label = f"BATTLE: {u1[:20]}... vs {u2[:20]}..."
                else:
                    u = entry['url'] or 'Unknown'
                    label = f"{u[:30]}..."
                
                with st.expander(f"{label} - {timestamp_formatted}"):
                    if entry['is_battle']:
                        st.markdown(f"**Battle Mode**")
                        st.markdown(f"• Brand A: `{entry['url']}`")
                        st.markdown(f"• Brand B: `{entry.get('url_2', 'N/A')}`")
                        st.markdown(f"• Assets A: {entry['image_count']}")
                        st.markdown(f"• Assets B: {entry.get('image_count_2', 0)}")
                    else:
                        st.markdown(f"**URL:** `{entry['url']}`")
                        st.markdown(f"**Assets:** {entry['image_count']}")
                        st.markdown(f"**Fonts:** {entry['stats_preview'].get('font_count', 0)}")
                    
                    # Color preview
                    if entry['stats_preview'].get('colors'):
                        colors_html = "".join([
                            f'<span style="background:{c};width:20px;height:20px;display:inline-block;margin-right:3px;border-radius:3px;"></span>'
                            for c in entry['stats_preview']['colors']
                        ])
                        st.markdown(f"**Colors:** {colors_html}", unsafe_allow_html=True)
                    
                    # Delete button
                    if st.button(f"Delete", key=f"del_{i}"):
                        HistoryManager.delete_scan(i)
                        st.rerun()
