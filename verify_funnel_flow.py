
import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            # Navigate to the Funnel Builder
            await page.goto("http://localhost:3000/funnels", timeout=120000)
            print("Successfully navigated to http://localhost:3000/funnels")

            # Wait for the empty state CTA to be visible
            await expect(page.locator('text=Crear Embudo')).to_be_visible(timeout=60000)
            print("Verified that the 'Crear Embudo' button is present in the empty state UI.")

            # Take a screenshot to verify the result
            await page.screenshot(path="funnel_flow_empty_state_verification.png")
            print("Screenshot captured as funnel_flow_empty_state_verification.png")

        except Exception as e:
            print(f"An error occurred: {e}")
            await page.screenshot(path="funnel_flow_error.png")
            print("Error screenshot captured as funnel_flow_error.png")

        finally:
            await browser.close()
            print("Browser closed.")

if __name__ == "__main__":
    asyncio.run(main())
