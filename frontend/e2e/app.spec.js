import { test, expect } from "@playwright/test";

test("full user flow", async ({ page }) => {
  const unique = Date.now();

  const username = `e2euser_${unique}`;
  const email = `e2e_${unique}@test.com`;
  const password = "password123"; // ≥ 7 chars (your backend rule)

  await page.goto("http://localhost:5173");

  // ---------- REGISTER ----------
  await page.fill("input[name=username]", username);
  await page.fill("input[name=email]", email);
  await page.fill("input[name=password]", password);
  await page.click("button:has-text('Register')");

  // ---------- LOGIN ----------
  await page.fill("input[name=username]", username);
  await page.fill("input[name=password]", password);
  await page.click("button:has-text('Login')");

  // Dashboard visible
  await expect(page.getByText("My Tasks")).toBeVisible();

  // ---------- CREATE TASK ----------
  await page.fill("input[placeholder='Title']", "Playwright Task");
  await page.fill("textarea", "E2E test");
  await page.click("button:has-text('Add Task')");

  await expect(page.getByText("Playwright Task")).toBeVisible();

  // ---------- COMPLETE TASK ----------
  await page.click("button:has-text('Complete')");

  await expect(page.getByText(/completed:/i)).toContainText("1");
});
