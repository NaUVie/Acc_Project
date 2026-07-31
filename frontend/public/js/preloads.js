
    (function() {
      var preconnectOrigins = ["https://cdn.shopify.com","https://extensions.shopifycdn.com"];
      var scripts = ["/cdn/shopifycloud/checkout-web/assets/c1/polyfills-legacy.DQk_-uDG.js","/cdn/shopifycloud/checkout-web/assets/c1/app-legacy.C6-V61xo.js","/cdn/shopifycloud/checkout-web/assets/c1/esnext-vendor-legacy.VxgM2yVk.js","/cdn/shopifycloud/checkout-web/assets/c1/context-browser-legacy.DlmlAbVh.js","/cdn/shopifycloud/checkout-web/assets/c1/useShopPayExternalAppContext-legacy.Chu4Wj1m.js","/cdn/shopifycloud/checkout-web/assets/c1/addresses-mailing-address-legacy.CsRvfU4n.js","/cdn/shopifycloud/checkout-web/assets/c1/payment-methods-filterAvailableMethods-legacy.DXZpRv9D.js","/cdn/shopifycloud/checkout-web/assets/c1/shop-pay-normalizeBuyerDetails-legacy.jVN1jx0L.js","/cdn/shopifycloud/checkout-web/assets/c1/graphql-UserPrivacySettingsSetMutation-legacy.DttapPdG.js","/cdn/shopifycloud/checkout-web/assets/c1/utils-getCommonShopPayExternalTelemetryAttributes-legacy.pFSelbJa.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useUnauthenticatedErrorModal-legacy.CGCX6Y2U.js","/cdn/shopifycloud/checkout-web/assets/c1/extensions-rpc-legacy.CVOcNXOS.js","/cdn/shopifycloud/checkout-web/assets/c1/graphql-PaymentSessionMutation-legacy.BO7n9UKr.js","/cdn/shopifycloud/checkout-web/assets/c1/hydrate-legacy.BsZQSaAs.js","/cdn/shopifycloud/checkout-web/assets/c1/utilities-browser-legacy.CHiGPLT2.js","/cdn/shopifycloud/checkout-web/assets/c1/locale-en-legacy.Cz0lv83q.js","/cdn/shopifycloud/checkout-web/assets/c1/OnePage-legacy.DM5uyMgx.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useWalletsTimeout-legacy.DjRdzzVe.js","/cdn/shopifycloud/checkout-web/assets/c1/MarketsProDisclaimer-legacy.Cev-wqAm.js","/cdn/shopifycloud/checkout-web/assets/c1/remember-me-hooks-legacy.CLxhFbBc.js","/cdn/shopifycloud/checkout-web/assets/c1/ShopLogo-legacy.C8s2M21k.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useHasOrdersFromMultipleShops-legacy.Ckc4mN2t.js","/cdn/shopifycloud/checkout-web/assets/c1/components-DeliveryTransition-legacy.DkBWBERd.js","/cdn/shopifycloud/checkout-web/assets/c1/ChangeCompanyLocationLink-legacy.Bm1CVU02.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useStableHostMethodsReferences-legacy.BMRFncAq.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useSandboxTelemetry-legacy.Dl1mCbm6.js","/cdn/shopifycloud/checkout-web/assets/c1/BillingAddressForm-legacy.DIhsREYH.js","/cdn/shopifycloud/checkout-web/assets/c1/PhoneField-legacy.BqGITs0u.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useCanChangeCompanyLocation-legacy.C6U-4uSA.js","/cdn/shopifycloud/checkout-web/assets/c1/EmptyState-legacy.D-924Cfv.js","/cdn/shopifycloud/checkout-web/assets/c1/Choice-legacy.BAaZJevt.js","/cdn/shopifycloud/checkout-web/assets/c1/Checkbox-legacy.FkdozIpc.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-usePostPurchase-legacy.CCO9MgvR.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useForceShopPayUrl-legacy.D1fGcdws.js","/cdn/shopifycloud/checkout-web/assets/c1/ButtonWithRegisterWebPixel-legacy.BJQovMO4.js","/cdn/shopifycloud/checkout-web/assets/c1/OffsitePaymentFailed-legacy.3a5zg5J9.js","/cdn/shopifycloud/checkout-web/assets/c1/ShopPayLogo-legacy.Bc7l_zWM.js","/cdn/shopifycloud/checkout-web/assets/c1/AutocompleteField-hooks-legacy.BM7IpaFm.js","/cdn/shopifycloud/checkout-web/assets/c1/PendingShipping-legacy.8IpY3rj_.js","/cdn/shopifycloud/checkout-web/assets/c1/ImpressionEventCapture-legacy.DnW0i_29.js","/cdn/shopifycloud/checkout-web/assets/c1/StoreCreditRedemption-StoreCreditRedemptionErrorBanner-legacy.LVogoSRB.js","/cdn/shopifycloud/checkout-web/assets/c1/PaymentIcon-legacy.DiH0fM2b.js","/cdn/shopifycloud/checkout-web/assets/c1/shop-cash-context-legacy.DZNHZFf_.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useGeneralPaymentErrorMessage-legacy.CY_wIQ7h.js","/cdn/shopifycloud/checkout-web/assets/c1/PaymentLine-legacy.Ctss4VtF.js","/cdn/shopifycloud/checkout-web/assets/c1/useShopPayButtonClassName-legacy.CZGxJp3C.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useShopPayProgressIntercepts-legacy.enNUOQMe.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useShowShopPayOptin-legacy.COKuXK8Y.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useUpdateCheckoutAddress-legacy.D6JVdSAS.js","/cdn/shopifycloud/checkout-web/assets/c1/Section-legacy.FlrBkAgq.js","/cdn/shopifycloud/checkout-web/assets/c1/useShopPaySessionTokenStorage-legacy.Cx7J4J7D.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useOnePageFormSubmit-legacy.Dk3YigIu.js","/cdn/shopifycloud/checkout-web/assets/c1/PaymentButtons-legacy.O6nMU4hE.js","/cdn/shopifycloud/checkout-web/assets/c1/useShopPayCheckoutGqlVersion-legacy.CzLWHZNt.js","/cdn/shopifycloud/checkout-web/assets/c1/shop-cash-monorail-legacy.Ds-HObN3.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useAvailableShopPromotionDiscount-legacy.BRCgPnl-.js","/cdn/shopifycloud/checkout-web/assets/c1/BillingAddressSelector-legacy.C32h-KnD.js","/cdn/shopifycloud/checkout-web/assets/c1/PaymentErrorBanner-legacy.BvDnEgab.js","/cdn/shopifycloud/checkout-web/assets/c1/Switch-legacy.FRmxHol2.js","/cdn/shopifycloud/checkout-web/assets/c1/shipping-rates-progressiveShippingRatesLoading-legacy.vqSgmDVe.js","/cdn/shopifycloud/checkout-web/assets/c1/ShipmentBreakdown-legacy.C4Sh9lJ5.js","/cdn/shopifycloud/checkout-web/assets/c1/MerchandiseModal-legacy.CH4NwRlc.js","/cdn/shopifycloud/checkout-web/assets/c1/extension-targets-shipping-options-legacy.CktwZ-Cz.js","/cdn/shopifycloud/checkout-web/assets/c1/EstimatedDeliveryContent-legacy.mxZl5WAq.js","/cdn/shopifycloud/checkout-web/assets/c1/ShippingMethodRateLabel-legacy.BVc2ba6t.js","/cdn/shopifycloud/checkout-web/assets/c1/ShippingMethodSelector-legacy.cR9iZKxg.js","/cdn/shopifycloud/checkout-web/assets/c1/TextArea-legacy.K2ReVzo5.js","/cdn/shopifycloud/checkout-web/assets/c1/SubscriptionPriceBreakdown-legacy.CFGtYtrB.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-usePaypalRowEffects-legacy.Dbdx6URB.js","/cdn/shopifycloud/checkout-web/assets/c1/Middot-legacy.BG2ADwjJ.js","/cdn/shopifycloud/checkout-web/assets/c1/StockProblems-StockProblemsLineItemList-legacy.BsH6_6bf.js","/cdn/shopifycloud/checkout-web/assets/c1/utilities-publishMessage-legacy.Du4DrXFC.js","/cdn/shopifycloud/checkout-web/assets/c1/component-RuntimeExtension-legacy.BXuLuH3k.js","/cdn/shopifycloud/checkout-web/assets/c1/AnnouncementRuntimeExtensions-legacy.C04M3DFo.js","/cdn/shopifycloud/checkout-web/assets/c1/QRCode-legacy.BXb5zdE7.js","/cdn/shopifycloud/checkout-web/assets/c1/utilities-dates-legacy.qoyDsntr.js","/cdn/shopifycloud/checkout-web/assets/c1/NumberField-legacy.C97_uzx2.js","/cdn/shopifycloud/checkout-web/assets/c1/extensions-remote-dom-legacy.C1yHbJOE.js","/cdn/shopifycloud/checkout-web/assets/c1/Sheet-legacy.C8iopYTO.js","/cdn/shopifycloud/checkout-web/assets/c1/extension-targets-rendering-extension-targets-legacy.YBV7O2QO.js","/cdn/shopifycloud/checkout-web/assets/c1/ExtensionsInner-legacy.CaV_ugRc.js","/cdn/shopifycloud/checkout-web/assets/c1/adapter-host-legacy.DsaNdP8U.js","/cdn/shopifycloud/checkout-web/assets/c1/sandbox.BNMWqM3S.worker.js","/cdn/shopifycloud/checkout-web/assets/c1/sandbox-2025-07.BU1xQJiP.worker.js","https://extensions.shopifycdn.com/shopifycloud/checkout-web/assets/c1/polyfills-entry-legacy.y34Tq78B.worker.js"];
      var styles = [];
      var fontPreconnectUrls = ["https://fonts.shopifycdn.com"];
      var fontPrefetchUrls = ["https://fonts.shopifycdn.com/roboto/roboto_n4.2019d890f07b1852f56ce63ba45b2db45d852cba.woff2?h1=c2tpbGxzYnJpZGdlLnZu&hmac=de3f9c9225a0cc7ed11a7567ea0191f09ebdc89752f386680b6d3a3a7e595b3c","https://fonts.shopifycdn.com/roboto/roboto_n5.250d51708d76acbac296b0e21ede8f81de4e37aa.woff2?h1=c2tpbGxzYnJpZGdlLnZu&hmac=5138157520566d77311c7ba98a19c60e2ee715614e913c34affd55bf19ab5bf2"];
      var imgPrefetchUrls = ["https://cdn.shopify.com/s/files/1/0672/5605/8167/files/Skills_Bridge_x320.png?v=1774434917"];

      function preconnect(url, callback) {
        var link = document.createElement('link');
        link.rel = 'dns-prefetch preconnect';
        link.href = url;
        link.crossOrigin = '';
        link.onload = link.onerror = callback;
        document.head.appendChild(link);
      }

      function preconnectAssets() {
        var resources = preconnectOrigins.concat(fontPreconnectUrls);
        var index = 0;
        (function next() {
          var res = resources[index++];
          if (res) preconnect(res, next);
        })();
      }

      function prefetch(url, as, callback) {
        var link = document.createElement('link');
        if (link.relList.supports('prefetch')) {
          link.rel = 'prefetch';
          link.fetchPriority = 'low';
          link.as = as;
          if (as === 'font') link.type = 'font/woff2';
          link.href = url;
          link.crossOrigin = '';
          link.onload = link.onerror = callback;
          document.head.appendChild(link);
        } else {
          var xhr = new XMLHttpRequest();
          xhr.open('GET', url, true);
          xhr.onloadend = callback;
          xhr.send();
        }
      }

      function prefetchAssets() {
        var resources = [].concat(
          scripts.map(function(url) { return [url, 'script']; }),
          styles.map(function(url) { return [url, 'style']; }),
          fontPrefetchUrls.map(function(url) { return [url, 'font']; }),
          imgPrefetchUrls.map(function(url) { return [url, 'image']; })
        );
        var index = 0;
        function run() {
          var res = resources[index++];
          if (res) prefetch(res[0], res[1], next);
        }
        var next = (self.requestIdleCallback || setTimeout).bind(self, run);
        next();
      }

      function onLoaded() {
        try {
          if (parseFloat(navigator.connection.effectiveType) > 2 && !navigator.connection.saveData) {
            preconnectAssets();
            prefetchAssets();
          }
        } catch (e) {}
      }

      if (document.readyState === 'complete') {
        onLoaded();
      } else {
        addEventListener('load', onLoaded);
      }
    })();
  