#!/usr/bin/env python3
"""
Capture screenshots of Fabrik Madrid tables page using Playwright
"""

import json
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 393, 'height': 852},  # Mobile viewport like in the CSS
            device_scale_factor=2
        )
        page = context.new_page()
        
        print("Navigating to page...")
        page.goto('https://emilianoechevarriafever.github.io/fabrik-madrid-tables/', 
                  wait_until='networkidle')
        
        # Wait for page to fully load
        page.wait_for_timeout(2000)
        
        # Take screenshot at top (hero + title)
        print("Taking screenshot 1: Top of page...")
        page.screenshot(path='fabrik-1-top.png')
        
        # Scroll to map section
        page.evaluate('window.scrollTo(0, 400)')
        page.wait_for_timeout(500)
        
        print("Taking screenshot 2: Map section...")
        page.screenshot(path='fabrik-2-map.png')
        
        # Scroll to ticket selector
        page.evaluate('window.scrollTo(0, 700)')
        page.wait_for_timeout(500)
        
        print("Taking screenshot 3: Ticket pills...")
        page.screenshot(path='fabrik-3-tickets.png')
        
        # Scroll further to see ticket items
        page.evaluate('window.scrollTo(0, 900)')
        page.wait_for_timeout(500)
        
        print("Taking screenshot 4: Ticket items...")
        page.screenshot(path='fabrik-4-ticket-items.png')
        
        # Get page state information
        print("\nAnalyzing page state...")
        
        page_info = page.evaluate('''() => {
            // Get selected tab
            const activePill = document.querySelector('.ticket-pill.active');
            const selectedTab = activePill ? activePill.textContent.trim() : 'None';
            
            // Get blue zones on map
            const blueZones = [];
            document.querySelectorAll('.map-zone.active').forEach(el => {
                blueZones.push({
                    id: el.getAttribute('data-zone'),
                    element: el.tagName
                });
            });
            
            // Check if pistaGroup is active (blue)
            const pistaGroup = document.getElementById('pistaGroup');
            const pistaActive = pistaGroup && pistaGroup.classList.contains('active');
            
            // Check for any other accidentally blue elements
            const allBlueElements = [];
            const svgElements = document.querySelectorAll('svg *[fill], svg *[style*="fill"]');
            svgElements.forEach(el => {
                const fill = window.getComputedStyle(el).fill;
                const computedColor = fill.toLowerCase();
                // Check for primary blue color (#0079ca or rgb(0, 121, 202))
                if (computedColor.includes('rgb(0, 121, 202)') || 
                    computedColor.includes('#0079ca')) {
                    allBlueElements.push({
                        id: el.id,
                        class: el.className.baseVal || el.className,
                        tag: el.tagName,
                        fill: computedColor
                    });
                }
            });
            
            // Get active ticket items
            const activeTickets = [];
            document.querySelectorAll('.tv-item.active').forEach(item => {
                activeTickets.push({
                    name: item.querySelector('.tv-name')?.textContent.trim(),
                    zone: item.getAttribute('data-zone')
                });
            });
            
            return {
                selectedTab,
                blueZones,
                pistaActive,
                allBlueElements: allBlueElements.slice(0, 20),
                activeTickets,
                url: window.location.href
            };
        }''')
        
        # Save analysis to JSON
        with open('fabrik-analysis.json', 'w') as f:
            json.dump(page_info, f, indent=2)
        
        print("\n" + "="*60)
        print("PAGE ANALYSIS REPORT")
        print("="*60)
        print(f"\n1. Selected Tab: {page_info['selectedTab']}")
        print(f"\n2. Blue Zones on Map (with .active class): {len(page_info['blueZones'])}")
        if page_info['blueZones']:
            for zone in page_info['blueZones']:
                print(f"   - {zone['id']}")
        else:
            print("   (None)")
        
        print(f"\n3. Pista Group Active (blue): {page_info['pistaActive']}")
        
        print(f"\n4. All Elements with Primary Blue Color: {len(page_info['allBlueElements'])}")
        if page_info['allBlueElements']:
            for el in page_info['allBlueElements'][:10]:
                print(f"   - {el['tag']} id='{el['id']}' class='{el['class']}'")
        
        print(f"\n5. Active Tickets Selected: {len(page_info['activeTickets'])}")
        if page_info['activeTickets']:
            for ticket in page_info['activeTickets']:
                print(f"   - {ticket['name']} (zone: {ticket['zone']})")
        
        print("\n" + "="*60)
        print("Screenshots saved:")
        print("- fabrik-1-top.png")
        print("- fabrik-2-map.png")
        print("- fabrik-3-tickets.png")
        print("- fabrik-4-ticket-items.png")
        print("- fabrik-analysis.json")
        print("="*60)
        
        # Close browser
        browser.close()

if __name__ == '__main__':
    main()
