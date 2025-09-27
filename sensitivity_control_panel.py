#!/usr/bin/env python3
"""
Sensitivity Control Panel - Easy interface for adjusting auto-fit parameters
Provides simple controls for fine-tuning the auto-fit behavior
"""

from configurable_autofit_generator import ConfigurableAutoFitGenerator, SENSITIVITY_PROFILES
from typing import Dict, Any

class SensitivityControlPanel:
    """
    Easy-to-use control panel for adjusting auto-fit sensitivity
    """
    
    def __init__(self):
        self.current_config = SENSITIVITY_PROFILES['balanced'].copy()
        print("🎛️ Sensitivity Control Panel Initialized")
        print("📊 Current settings: BALANCED profile")
    
    def load_profile(self, profile_name: str) -> None:
        """Load a predefined sensitivity profile"""
        if profile_name not in SENSITIVITY_PROFILES:
            print(f"❌ Unknown profile: {profile_name}")
            print(f"Available profiles: {list(SENSITIVITY_PROFILES.keys())}")
            return
        
        self.current_config = SENSITIVITY_PROFILES[profile_name].copy()
        print(f"✅ Loaded {profile_name.upper()} sensitivity profile")
        self.show_current_settings()
    
    def adjust_sensitivity(self, parameter: str, value: Any) -> None:
        """Adjust a specific sensitivity parameter"""
        if parameter not in self.current_config:
            print(f"❌ Unknown parameter: {parameter}")
            self.show_available_parameters()
            return
        
        old_value = self.current_config[parameter]
        self.current_config[parameter] = value
        print(f"✅ Updated {parameter}: {old_value} → {value}")
    
    def batch_adjust(self, adjustments: Dict[str, Any]) -> None:
        """Adjust multiple parameters at once"""
        print("🔧 Applying batch adjustments...")
        for param, value in adjustments.items():
            if param in self.current_config:
                old_value = self.current_config[param]
                self.current_config[param] = value
                print(f"   {param}: {old_value} → {value}")
            else:
                print(f"   ⚠️ Skipped unknown parameter: {param}")
    
    def show_current_settings(self) -> None:
        """Display current sensitivity settings"""
        print("\n🎛️ CURRENT SENSITIVITY SETTINGS:")
        print("=" * 50)
        
        # Key thresholds
        print("📏 Content Thresholds (lines):")
        print(f"   Short resume: ≤ {self.current_config['short_resume_lines']} lines")
        print(f"   Medium resume: ≤ {self.current_config['medium_resume_lines']} lines") 
        print(f"   Long resume: ≤ {self.current_config['long_resume_lines']} lines")
        print(f"   Very long: ≤ {self.current_config['very_long_lines']} lines")
        
        # Sensitivity settings
        print(f"\n⚖️ Scaling Behavior:")
        print(f"   Overall sensitivity: {self.current_config['scaling_sensitivity']:.1f}x")
        print(f"   Font size range: {self.current_config['min_font_size']}-{self.current_config['max_font_size']}pt")
        print(f"   Spacing reduction: {self.current_config['spacing_reduction']:.1f}x")
        print(f"   Margin reduction: {self.current_config['margin_reduction']:.1f}x")
        
        # Font sizes per level
        print(f"\n📝 Font Sizes by Level:")
        for level in ['comfortable', 'balanced', 'compact', 'dense', 'ultra_dense']:
            if level in self.current_config:
                fonts = self.current_config[level]
                print(f"   {level.replace('_', ' ').title()}: Body={fonts['body']}pt, Header={fonts['header']}pt")
        
        print("=" * 50)
    
    def show_available_parameters(self) -> None:
        """Show all available parameters that can be adjusted"""
        print("\n🔧 ADJUSTABLE PARAMETERS:")
        print("=" * 40)
        
        categories = {
            "Content Thresholds": ['short_resume_lines', 'medium_resume_lines', 'long_resume_lines', 'very_long_lines'],
            "Scaling Control": ['scaling_sensitivity', 'min_font_size', 'max_font_size'],
            "Spacing Control": ['spacing_reduction', 'margin_reduction'],
            "Content Weights": ['header_weight', 'bullet_weight', 'job_entry_weight', 'word_weight', 'line_weight']
        }
        
        for category, params in categories.items():
            print(f"\n📊 {category}:")
            for param in params:
                if param in self.current_config:
                    print(f"   {param}: {self.current_config[param]}")
        
        print("\n💡 Usage: control_panel.adjust_sensitivity('parameter_name', new_value)")
    
    def create_generator(self) -> ConfigurableAutoFitGenerator:
        """Create a generator with current settings"""
        return ConfigurableAutoFitGenerator(self.current_config)
    
    def quick_presets(self) -> None:
        """Show quick preset adjustments"""
        print("\n🚀 QUICK PRESET ADJUSTMENTS:")
        print("=" * 40)
        print("💡 Use these for common scenarios:\n")
        
        presets = {
            "More Conservative": {
                'scaling_sensitivity': 0.8,
                'short_resume_lines': 30,
                'medium_resume_lines': 50
            },
            "More Aggressive": {
                'scaling_sensitivity': 1.2,
                'short_resume_lines': 20,
                'medium_resume_lines': 35
            },
            "Larger Fonts": {
                'min_font_size': 8,
                'comfortable': {'header': 20, 'section': 14, 'body': 12, 'small': 10}
            },
            "Smaller Fonts": {
                'min_font_size': 5,
                'comfortable': {'header': 16, 'section': 11, 'body': 9, 'small': 7}
            },
            "More Spacing": {
                'spacing_reduction': 1.0,
                'margin_reduction': 1.0
            },
            "Less Spacing": {
                'spacing_reduction': 0.6,
                'margin_reduction': 0.7
            }
        }
        
        for preset_name, settings in presets.items():
            print(f"🎛️ {preset_name}:")
            for param, value in settings.items():
                print(f"   control_panel.adjust_sensitivity('{param}', {value})")
            print()
    
    def test_current_config(self, test_resume: str | None = None) -> None:
        """Test current configuration with sample resume"""
        if test_resume is None:
            test_resume = """# Test Resume
test@email.com | (555) 123-4567

## Summary
**Software Engineer** with **5+ years** experience in *full-stack development*.

## Experience
**Senior Developer**
*Tech Company | 2020 - Present*
- Built **scalable applications** serving `1M+ users`
- **Achievement**: Reduced latency by *50%*

## Skills
**Languages:** `Python`, **JavaScript**, *TypeScript*"""

        print(f"\n🧪 Testing current configuration...")
        
        try:
            generator = self.create_generator()
            result = generator.generate_configurable_docx_base64(test_resume)
            print(f"✅ Test successful: {len(result):,} characters generated")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")

# Example usage and demonstrations
def demo_sensitivity_controls():
    """Demonstrate how to use the sensitivity controls"""
    
    print("🎛️ SENSITIVITY CONTROL PANEL DEMO")
    print("=" * 60)
    
    # Create control panel
    control_panel = SensitivityControlPanel()
    
    # Show initial settings
    control_panel.show_current_settings()
    
    # Demo: Load different profile
    print(f"\n🔄 Loading CONSERVATIVE profile...")
    control_panel.load_profile('conservative')
    
    # Demo: Individual adjustments
    print(f"\n🔧 Making individual adjustments...")
    control_panel.adjust_sensitivity('scaling_sensitivity', 0.6)
    control_panel.adjust_sensitivity('min_font_size', 8)
    
    # Demo: Batch adjustments
    print(f"\n🔧 Making batch adjustments...")
    control_panel.batch_adjust({
        'short_resume_lines': 35,
        'medium_resume_lines': 55,
        'spacing_reduction': 0.95
    })
    
    # Test configuration
    control_panel.test_current_config()
    
    # Show quick presets
    control_panel.quick_presets()
    
    print(f"\n🎉 Demo complete! Control panel is ready to use.")
    return control_panel

if __name__ == "__main__":
    # Run the demo
    panel = demo_sensitivity_controls()
    
    print(f"\n💡 HOW TO USE IN YOUR CODE:")
    print("=" * 40)
    print("""
# 1. Create control panel
control_panel = SensitivityControlPanel()

# 2. Load a profile or adjust settings
control_panel.load_profile('aggressive')  # or 'conservative', 'balanced'

# 3. Fine-tune individual parameters
control_panel.adjust_sensitivity('scaling_sensitivity', 1.1)
control_panel.adjust_sensitivity('min_font_size', 7)

# 4. Create generator with your settings
generator = control_panel.create_generator()

# 5. Generate resume
result = generator.generate_configurable_docx_base64(your_resume_markdown)
""")