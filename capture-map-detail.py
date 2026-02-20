#!/usr/bin/env python3
"""
Capture focused screenshot of the map area
"""

import json
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 393, 'height': 1200},  # Taller viewport
            device_scale_factor=2
        )
        page = context.new_page()
        
        print("Navigating to page...")
        page.goto('https://emilianoechevarriafever.github.io/fabrik-madrid-tables/', 
                  wait_until='networkidle')
        
        page.wait_for_timeout(2000)
        
        # Scroll to where map is visible
        page.evaluate('window.scrollTo(0, 600)')
        page.wait_for_timeout(1000)
        
        print("Taking map + ticket pills screenshot...")
        page.screenshot(path='fabrik-map-detailed.png')
        
        # Get more detailed information about the pistaGroup
        pista_info = page.evaluate('''() => {
            const pistaGroup = document.getElementById('pistaGroup');
            if (!pistaGroup) return { exists: false };
            
            const children = [];
            pistaGroup.querySelectorAll('*').forEach((child, idx) => {
                if (idx < 10) {  // First 10 children
                    const style = window.getComputedStyle(child);
                    children.push({
                        tag: child.tagName,
                        id: child.id,
                        class: child.className.baseVal || child.className,
                        fill: style.fill,
                        computedFill: style.fill
                    });
                }
            });
            
            return {
                exists: true,
                id: pistaGroup.id,
                hasActiveClass: pistaGroup.classList.contains('active'),
                classList: Array.from(pistaGroup.classList),
                children: children,
                innerHTML: pistaGroup.innerHTML.substring(0, 500)
            };
        }''')
        
        print("\n" + "="*60)
        print("PISTA GROUP DETAILS")
        print("="*60)
        print(json.dumps(pista_info, indent=2))
        
        with open('pista-info.json', 'w') as f:
            json.dump(pista_info, f, indent=2)
        
        print("\nScreenshot saved: fabrik-map-detailed.png")
        print("Analysis saved: pista-info.json")
        
        browser.close()

if __name__ == '__main__':
    main()
