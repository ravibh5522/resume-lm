# 🎛️ Sensitivity Configuration Guide

## How to Adjust Auto-Fit Sensitivity Controls

Your resume generator now has **configurable sensitivity controls** that let you fine-tune exactly when and how much font scaling occurs to fit resumes on a single page.

## 🚀 Quick Setup

In your `main.py`, you can adjust these parameters:

```python
# PDF Generator Sensitivity
pdf_generator = create_configurable_generators(
    sensitivity_level="balanced",    # 'conservative', 'balanced', or 'aggressive'
    custom_adjustments={
        'scaling_sensitivity': 1.1,     # How aggressive: 0.5 (gentle) to 2.0 (aggressive)
        'min_font_size': 7,             # Minimum font size: 5-10pt
        'short_resume_lines': 22,       # When to start scaling: 15-35 lines
        'spacing_reduction': 0.75,      # Spacing: 0.5 (tight) to 1.0 (loose)
    }
)

# DOCX Generator Sensitivity
docx_generator = create_configurable_generators(
    sensitivity_level="balanced", 
    custom_adjustments={
        'scaling_sensitivity': 1.0,     # Standard scaling for DOCX
        'min_font_size': 8,             # Bit larger minimum for Word
        'short_resume_lines': 25,       # Allow more lines in DOCX
        'spacing_reduction': 0.8,       # Keep more spacing in DOCX
    }
)
```

## 🎯 Parameter Guide

### 1. **scaling_sensitivity** (0.5 - 2.0)
- **0.5**: Very gentle scaling - keeps fonts larger
- **1.0**: Standard scaling - balanced approach
- **1.5**: Aggressive scaling - willing to make fonts smaller
- **2.0**: Maximum scaling - prioritizes single-page fit

### 2. **min_font_size** (5 - 10)
- **5pt**: Allows very small fonts (hard to read)
- **7pt**: Good balance between readability and space
- **9pt**: Prioritizes readability over space
- **10pt**: Maximum readability, may not fit long resumes

### 3. **short_resume_lines** (15 - 35)
- **15**: Start scaling very early (very aggressive)
- **22**: Start scaling for medium-length resumes
- **30**: Only scale for longer resumes
- **35**: Very conservative, only scale when necessary

### 4. **spacing_reduction** (0.5 - 1.0)
- **0.5**: Remove most spacing (very tight)
- **0.75**: Moderate spacing reduction
- **0.9**: Keep most spacing
- **1.0**: No spacing reduction

## 📊 Sensitivity Profiles

### 🐌 Conservative Profile
```python
sensitivity_level="conservative"
# Keeps fonts large, starts scaling late, preserves spacing
# Best for: Readability priority, shorter resumes
```

### ⚖️ Balanced Profile  
```python
sensitivity_level="balanced"
# Good balance between readability and single-page fit
# Best for: Most use cases, general purpose
```

### 🚀 Aggressive Profile
```python
sensitivity_level="aggressive"
# Scales more aggressively, allows smaller fonts
# Best for: Long resumes, maximum content density
```

## 🔧 Common Adjustments

### Make it **MORE** aggressive (smaller fonts, better fit):
```python
custom_adjustments={
    'scaling_sensitivity': 1.4,    # More aggressive
    'min_font_size': 6,            # Allow smaller fonts
    'short_resume_lines': 18,      # Start scaling earlier
    'spacing_reduction': 0.6,      # Reduce spacing more
}
```

### Make it **LESS** aggressive (larger fonts, better readability):
```python
custom_adjustments={
    'scaling_sensitivity': 0.8,    # More gentle
    'min_font_size': 8,            # Keep fonts readable
    'short_resume_lines': 30,      # Scale only when needed
    'spacing_reduction': 0.9,      # Keep more spacing
}
```

### For **very long resumes** (prioritize fitting):
```python
custom_adjustments={
    'scaling_sensitivity': 1.6,    # Very aggressive
    'min_font_size': 5,            # Allow tiny fonts
    'short_resume_lines': 15,      # Scale early
    'spacing_reduction': 0.5,      # Minimal spacing
}
```

### For **readability priority** (prioritize font size):
```python
custom_adjustments={
    'scaling_sensitivity': 0.6,    # Very gentle
    'min_font_size': 9,            # Large minimum font
    'short_resume_lines': 35,      # Scale very late
    'spacing_reduction': 0.95,     # Keep all spacing
}
```

## 🧪 Testing Different Settings

You can test different sensitivity levels using the provided example:

```bash
python sensitivity_integration_example.py
```

This will show you how different settings affect the same resume content.

## 🎛️ Advanced Control

For complete control, use the `SensitivityControlPanel` directly:

```python
from sensitivity_control_panel import SensitivityControlPanel

# Create control panel
control = SensitivityControlPanel()

# Load a profile
control.load_profile('balanced')

# Make individual adjustments
control.adjust_sensitivity('scaling_sensitivity', 1.2)
control.adjust_sensitivity('min_font_size', 7)

# Or batch adjustments
control.batch_adjust({
    'scaling_sensitivity': 1.2,
    'short_resume_lines': 20,
    'spacing_reduction': 0.7
})

# Create generator
generator = control.create_generator()
```

## 💡 Best Practices

1. **Start with 'balanced'** and adjust from there
2. **Test with your typical resume content** to see what works
3. **Consider your audience** - some prefer readability over single-page fit
4. **Use different settings for PDF vs DOCX** if needed
5. **Monitor user feedback** to find the sweet spot

## 📈 Monitoring Results

The system will output information like:
```
🎯 Configurable scaling: DENSE - Body: 7pt, Spacing: 1pt
✅ Configurable auto-fit DOCX: 52,248 chars, Level: DENSE
```

This tells you:
- **Level used**: COMFORTABLE, BALANCED, COMPACT, DENSE, ULTRA_DENSE
- **Font sizes**: What body and header sizes were used
- **Output size**: Character count of generated document

Use this information to tune your settings for optimal results!