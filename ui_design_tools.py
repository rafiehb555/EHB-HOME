import argparse
import base64
import io
import json
import os
import sys
from typing import Any, Dict, List, Optional

import requests
from PIL import Image

from backend.api_integrations import Config, service_manager

#!/usr/bin/env python3
"""
EHB Home Page - UI Design Tools
Convert UI design images to React components
"""

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

class UIDesignAnalyzer:
    """Analyze UI design images and generate React components"""




    def __init__(self):
        self.ai_service = service_manager.ai

    async def analyze_design_image(self, image_path: str) -> Dict[str, Any]:
        """Analyze a UI design image and extract design information"""
        try:
            # Read and encode image
            with open(image_path, 'rb') as f:
                image_data = f.read()
                image_base64 = base64.b64encode(image_data).decode('utf-8')

            # Analyze image using AI
            prompt = f"""
            Analyze this UI design image and provide a detailed breakdown:

            1. Layout structure (header, main content, sidebar, footer)
            2. Color scheme and typography
            3. Component types (buttons, forms, cards, navigation)
            4. Spacing and alignment
            5. Interactive elements
            6. Responsive design considerations

            Return the analysis as JSON with the following structure:
            {{
                "layout": {{
                    "type": "string",
                    "sections": ["array of section names"],
                    "grid_system": "string"
                }},
                "colors": {{
                    "primary": "string",
                    "secondary": "string",
                    "background": "string",
                    "text": "string"
                }},
                "components": [
                    {{
                        "type": "string",
                        "name": "string",
                        "props": {{}},
                        "styling": {{}}
                    }}
                ],
                "typography": {{
                    "font_family": "string",
                    "font_sizes": {{}},
                    "font_weights": {{}}
                }},
                "spacing": {{
                    "unit": "string",
                    "scale": []
                }}
            }}
            """

            # Use OpenAI to analyze the image
            response = await self.ai_service.generate_openai_text(prompt)

            if response['success']:
                # Parse the JSON response
                try:
                    analysis = json.loads(response['text'])
                    return {
                        'success': True,
                        'analysis': analysis,
                        'image_path': image_path
                    }
                except json.JSONDecodeError:
                    return {
                        'success': False,
                        'error': 'Failed to parse AI response as JSON'
                    }
            else:
                return response

        except Exception as e:
            return {
                'success': False,
                'error': f'Image analysis failed: {str(e)}'
            }

    async def generate_react_component(self, analysis: Dict[str, Any], component_name: str = "DesignComponent") -> str:
        """Generate React component code from design analysis"""
        try:
            prompt = f"""
            Generate a React component based on this UI design analysis:

            {json.dumps(analysis, indent=2)}

            Create a complete React component with:
            1. Proper TypeScript types
            2. Tailwind CSS classes based on the design
            3. Responsive design
            4. Accessibility features
            5. Modern React patterns (hooks, etc.)
            6. Framer Motion animations where appropriate

            Component name: {component_name}

            Return only the React component code, no explanations.
            """

            response = await self.ai_service.generate_openai_text(prompt)

            if response['success']:
                return response['text']
            else:
                return f"// Error generating component: {response.get('error', 'Unknown error')}"

        except Exception as e:
            return f"// Error generating component: {str(e)}"

    async def generate_storybook_story(self, component_name: str, analysis: Dict[str, Any]) -> str:
        """Generate Storybook story for the component"""
        try:
            prompt = f"""
            Generate a Storybook story for the React component '{component_name}' based on this design analysis:

            {json.dumps(analysis, indent=2)}

            Create a comprehensive Storybook story with:
            1. Multiple variants/states
            2. Proper controls
            3. Documentation
            4. Accessibility testing

            Return only the Storybook story code.
            """

            response = await self.ai_service.generate_openai_text(prompt)

            if response['success']:
                return response['text']
            else:
                return f"// Error generating story: {response.get('error', 'Unknown error')}"

        except Exception as e:
            return f"// Error generating story: {str(e)}"

    async def generate_tailwind_config(self, analysis: Dict[str, Any]) -> str:
        """Generate Tailwind CSS configuration based on design analysis"""
        try:
            colors = analysis.get('colors', {})
            typography = analysis.get('typography', {})
            spacing = analysis.get('spacing', {})

            config = {
                "theme": {
                    "extend": {
                        "colors": {
                            "primary": colors.get('primary', '#3B82F6'),
                            "secondary": colors.get('secondary', '#6B7280'),
                            "background": colors.get('background', '#FFFFFF'),
                            "text": colors.get('text', '#1F2937')
                        },
                        "fontFamily": {
                            "sans": typography.get('font_family', 'Inter').split(',')
                        },
                        "fontSize": typography.get('font_sizes', {}),
                        "fontWeight": typography.get('font_weights', {}),
                        "spacing": spacing.get('scale', {})
                    }
                }
            }

            return f"""
// tailwind.config.js
module.exports = {json.dumps(config, indent=2)}
            """.strip()

        except Exception as e:
            return f"// Error generating Tailwind config: {str(e)}"

    async def create_component_files(self, image_path: str, output_dir: str = "generated_components") -> Dict[str, Any]:
        """Create complete component files from design image"""
        try:
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)

            # Analyze the design image
            analysis_result = await self.analyze_design_image(image_path)

            if not analysis_result['success']:
                return analysis_result

            analysis = analysis_result['analysis']
            component_name = os.path.splitext(os.path.basename(image_path))[0].replace(' ', '').title()

            # Generate component code
            component_code = await self.generate_react_component(analysis, component_name)

            # Generate storybook story
            story_code = await self.generate_storybook_story(component_name, analysis)

            # Generate Tailwind config
            tailwind_config = await self.generate_tailwind_config(analysis)

            # Create files
            files_created = []

            # Component file
            component_file = os.path.join(output_dir, f"{component_name}.tsx")
            with open(component_file, 'w', encoding='utf-8') as f:
                f.write(component_code)
            files_created.append(component_file)

            # Storybook story file
            story_file = os.path.join(output_dir, f"{component_name}.stories.tsx")
            with open(story_file, 'w', encoding='utf-8') as f:
                f.write(story_code)
            files_created.append(story_file)

            # Tailwind config file
            config_file = os.path.join(output_dir, f"tailwind.config.{component_name}.js")
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(tailwind_config)
            files_created.append(config_file)

            # Analysis JSON file
            analysis_file = os.path.join(output_dir, f"{component_name}_analysis.json")
            with open(analysis_file, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2)
            files_created.append(analysis_file)

            return {
                'success': True,
                'component_name': component_name,
                'files_created': files_created,
                'analysis': analysis
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to create component files: {str(e)}'
            }

class DesignSystemGenerator:
    """Generate a complete design system from multiple images"""




    def __init__(self):
        self.analyzer = UIDesignAnalyzer()

    async def generate_design_system(self, image_directory: str, output_dir: str = "design_system") -> Dict[str, Any]:
        """Generate a complete design system from multiple design images"""
        try:
            os.makedirs(output_dir, exist_ok=True)

            # Get all image files
            image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']
            image_files = []

            for file in os.listdir(image_directory):
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    image_files.append(os.path.join(image_directory, file))

            if not image_files:
                return {
                    'success': False,
                    'error': 'No image files found in directory'
                }

            # Analyze all images
            all_analyses = []
            components_created = []

            for image_file in image_files:
                print(f"🔍 Analyzing: {os.path.basename(image_file)}")

                result = await self.analyzer.create_component_files(image_file, output_dir)

                if result['success']:
                    all_analyses.append(result['analysis'])
                    components_created.append(result['component_name'])
                    print(f"✅ Created component: {result['component_name']}")
                else:
                    print(f"❌ Failed to create component: {result.get('error', 'Unknown error')}")

            # Generate design system documentation
            design_system_doc = await self.generate_design_system_doc(all_analyses, components_created)

            # Create design system index
            index_file = os.path.join(output_dir, "index.ts")
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(self.generate_component_index(components_created))

            # Create design system documentation
            doc_file = os.path.join(output_dir, "DESIGN_SYSTEM.md")
            with open(doc_file, 'w', encoding='utf-8') as f:
                f.write(design_system_doc)

            return {
                'success': True,
                'components_created': components_created,
                'total_components': len(components_created),
                'output_directory': output_dir,
                'analyses': all_analyses
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to generate design system: {str(e)}'
            }

    async def generate_design_system_doc(self, analyses: List[Dict[str, Any]], components: List[str]) -> str:
        """Generate design system documentation"""
        try:
            prompt = f"""
            Generate comprehensive design system documentation based on these component analyses:

            {json.dumps(analyses, indent=2)}

            Create a markdown document with:
            1. Design principles
            2. Color palette
            3. Typography scale
            4. Component library
            5. Usage guidelines
            6. Accessibility standards

            Components: {', '.join(components)}

            Return only the markdown documentation.
            """

            response = await self.analyzer.ai_service.generate_openai_text(prompt)

            if response['success']:
                return response['text']
            else:
                return f"# Design System Documentation\n\nError generating documentation: {response.get('error', 'Unknown error')}"

        except Exception as e:
            return f"# Design System Documentation\n\nError generating documentation: {str(e)}"

    def generate_component_index(self, components: List[str]) -> str:
        """Generate component index file"""
        index_content = "// Design System Component Index\n\n"

        for component in components:
            index_content += f"export {{ default as {component} }} from './{component}';\n"

        return index_content

async def main():
    """Main function for testing the UI design tools"""
    print("🎨 EHB UI Design Tools")
    print("=" * 50)

    # Initialize the analyzer
    analyzer = UIDesignAnalyzer()

    # Test with a sample image (if available)
    test_image = "sample_design.png"

    if os.path.exists(test_image):
        print(f"🔍 Testing with image: {test_image}")

        # Analyze the image
        analysis_result = await analyzer.analyze_design_image(test_image)

        if analysis_result['success']:
            print("✅ Image analysis successful")

            # Generate component files
            result = await analyzer.create_component_files(test_image)

            if result['success']:
                print(f"✅ Generated component: {result['component_name']}")
                print(f"📁 Files created: {len(result['files_created'])}")
                for file in result['files_created']:
                    print(f"   - {file}")
            else:
                print(f"❌ Failed to generate component: {result.get('error', 'Unknown error')}")
        else:
            print(f"❌ Image analysis failed: {analysis_result.get('error', 'Unknown error')}")
    else:
        print("ℹ️  No test image found. Use the tools with your own design images.")
        print("\nUsage:")
        print("1. Place your UI design images in a directory")
        print("2. Run: python ui_design_tools.py --analyze <image_path>")
        print("3. Or run: python ui_design_tools.py --generate-system <directory>")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EHB UI Design Tools")
    parser.add_argument("--analyze", help="Analyze a single design image")
    parser.add_argument("--generate-system", help="Generate design system from directory")
    parser.add_argument("--output", default="generated_components", help="Output directory")

    args = parser.parse_args()

    if args.analyze:
        # Analyze single image
        analyzer = UIDesignAnalyzer()
        result = asyncio.run(analyzer.create_component_files(args.analyze, args.output))
        print(json.dumps(result, indent=2))
    elif args.generate_system:
        # Generate design system
        generator = DesignSystemGenerator()
        result = asyncio.run(generator.generate_design_system(args.generate_system, args.output))
        print(json.dumps(result, indent=2))
    else:
        # Run default test
        asyncio.run(main())
