
import asyncio
import json
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            # --- 1. Log In ---
            print("Navigating to login page...")
            await page.goto("http://localhost:3000/", timeout=120000)

            print("Entering credentials...")
            await page.fill('input[type="email"]', 'test@example.com')
            await page.fill('input[type="password"]', 'testpassword')

            print("Clicking login button...")
            await page.click('button[type="submit"]')

            # --- 2. Verify Successful Login ---
            print("Waiting for main application to load after login...")
            # After login, the app defaults to the Funnels view. We wait for its title.
            await expect(page.locator('h2:has-text("Arquitecto de Embudos")')).to_be_visible(timeout=60000)
            print("Login successful. Main application is visible.")

            # --- 3. Navigate to CRM View ---
            print("Navigating to the CRM view...")
            await page.click('button:has-text("Ventas y CRM")')

            # --- 4. Verify CRM Empty State ---
            print("Verifying CRM empty state UI...")
            await expect(page.locator('text=Crear Oportunidad')).to_be_visible(timeout=60000)
            print("Successfully verified the 'Crear Oportunidad' button is present.")

            await page.screenshot(path="crm_flow_empty_state_verification.png")
            print("Screenshot of successful verification captured as crm_flow_empty_state_verification.png")

        except Exception as e:
            print(f"An error occurred: {e}")
            await page.screenshot(path="crm_flow_error.png")
            print("Error screenshot captured as crm_flow_error.png")

        finally:
            await browser.close()
            print("Browser closed.")

if __name__ == "__main__":
    asyncio.run(main())
