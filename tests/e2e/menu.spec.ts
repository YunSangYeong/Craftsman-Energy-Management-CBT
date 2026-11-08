import { test, expect } from '@playwright/test';
for (const size of [{width:390,height:480},{width:740,height:360}]) {
 test(`menu wheel reaches bottom and returns to dashboard ${size.width}x${size.height}`, async({page})=>{
  await page.setViewportSize(size); await page.goto('');
  await page.getByRole('button',{name:'메뉴 열기'}).click();
  await page.waitForTimeout(400);
  const menu=page.locator('.sidebar');
  await menu.hover(); await page.mouse.wheel(0,1600);
  await expect.poll(()=>menu.evaluate(e=>e.scrollTop)).toBeGreaterThan(0);
  const reset=menu.getByRole('button',{name:'데이터 초기화',exact:true});
  await expect(reset).toBeInViewport();
  await reset.click(); await expect(page.getByRole('dialog')).toBeVisible();
  await page.getByRole('button',{name:'돌아가기',exact:true}).click();
  // Reset closes the menu; reopen before reverse input.
  if(!await menu.getByRole('button',{name:'학습 대시보드',exact:true}).isVisible()) await page.getByRole('button',{name:'메뉴 열기'}).click();
  await page.waitForTimeout(400); await menu.hover(); await page.mouse.wheel(0,-1600);
  await expect.poll(()=>menu.evaluate(e=>e.scrollTop)).toBe(0);
  await menu.getByRole('button',{name:'학습 대시보드',exact:true}).click();
  await expect(page.getByRole('heading',{name:'에너지관리기능사 필기 CBT',exact:true})).toBeVisible();
 });
 test(`menu actual touch swipe both directions ${size.width}x${size.height}`,async({page,isMobile})=>{
  test.skip(!isMobile,'Touch separately verified in Pixel 7 Chromium emulation');
  await page.setViewportSize(size); await page.goto('');
  await page.getByRole('button',{name:'메뉴 열기'}).tap();await page.waitForTimeout(400);
  const cdp=await page.context().newCDPSession(page);
  async function swipe(from:number,to:number) {
   await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:130,y:from}]});
   for(let i=1;i<=12;i++) { await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:130,y:from+(to-from)*i/12}]});await page.waitForTimeout(20); }
   await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});await page.waitForTimeout(300);
  }
  for(let i=0;i<4;i++) await swipe(size.height-50,70);
  const menu=page.locator('.sidebar');
  await expect.poll(()=>menu.evaluate(e=>e.scrollTop)).toBeGreaterThan(0);
  await expect(menu.getByRole('button',{name:'학습 기록 백업'})).toBeInViewport();
  await expect(menu.getByRole('button',{name:'데이터 초기화',exact:true})).toBeInViewport();
  const download=page.waitForEvent('download'); await menu.getByRole('button',{name:'학습 기록 백업'}).tap(); await download;
  for(let i=0;i<4;i++) await swipe(70,size.height-50);
  await expect.poll(()=>menu.evaluate(e=>e.scrollTop)).toBe(0);
  await menu.getByRole('button',{name:'학습 대시보드',exact:true}).tap();
  await expect(page.getByRole('heading',{name:'에너지관리기능사 필기 CBT',exact:true})).toBeVisible();
 });
}
