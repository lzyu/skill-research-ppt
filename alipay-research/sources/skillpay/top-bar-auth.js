(function () {
  const ACCOUNT_REFRESH_EVENT = "aipay-account-refresh";
  const AUTHCENTER_RETURN_PARAM = "aipay_authcenter_login";
  const AUTHCENTER_LOGOUT_RETURN_VALUE = "logout";
  const LOGIN_EXPIRED_ERROR_CODE = "006";
  const LOGOUT_FALLBACK_ORIGIN = "https://skillpay.alipay.com";
  const ONBOARDING_STORAGE_KEY = "aipay:onboarding-state";
  const LOGIN_ENTRY_HREF = "/?aipay_login=1&aipay_login_next=stay";
  const PAGE_EXPOSURE_CODE = 1001;
  const ACCOUNT_INFO_CACHE_TTL_MS = 500;
  const SKILLPAY_SESSION_ENDPOINT = "/api/auth/session";
  const SKILLPAY_LOGOUT_ENDPOINT = "/api/auth/logout";
  const NAV_ACCOUNT_CACHE_KEY = "aipay:nav-account-cache";
  const NAV_ACCOUNT_CACHE_VERSION = 1;
  const NAV_ACCOUNT_CACHE_TTL_MS = 30 * 60 * 1000;
  const USER_MENU_CLOSE_DELAY_MS = 220;
  const YUYAN_MONITOR_ID = "180020010001296536";
  const YUYAN_MONITOR_UMD_URL =
    "https://gw.alipayobjects.com/os/lib/alipay/yuyan-monitor-sdk/1.0.6/dist/index.umd.min.js";
  const API_BASES = {
    pre: "https://aipayapi-pre.alipay.com",
    prod: "https://aipayapi.alipay.com",
  };
  const DEFAULT_DEV_WATCHTOWER_ORIGIN =
    "https://webgw.stable.alipay.net/watchtowerproxy/proxy";
  const DEFAULT_DEV_API_TARGET = "http://aipayweb-37.rz00b.dev.alipay.net";
  const WATCHTOWER_PROXY_TARGET_HEADER = "x-watchtowerproxy-target-origin";
  const WEBGW_VERSION = "2.0";
  const WEBGW_APP_ID = "180020010001296536";
  const CONFIGURED_OPENBRIDGE_ENV = "";
  const DEFAULT_AIPAY_API_RUNTIME_CONFIG = {
    useLocalApiProxy: false,
    devWatchtowerOrigin: DEFAULT_DEV_WATCHTOWER_ORIGIN,
    devApiTarget: DEFAULT_DEV_API_TARGET,
    webgwVersion: WEBGW_VERSION,
    webgwAppId: WEBGW_APP_ID,
  };
  const LOCAL_API_PROXY_HOSTS = new Set([
    "localhost",
    "127.0.0.1",
    "::1",
    "local.dev.alipay.net",
    "aipay-pre-local.alipay.com",
  ]);
  const AUTHCENTER_ORIGINS = {
    dev: "https://authcenter.stable.alipay.net",
    pre: "https://authcenter-pre.alipay.com",
    prod: "https://auth.alipay.com",
  };
  const ALLOWED_LOGOUT_GOTO_RULES = [
    {
      domains: [
        "zhisheng",
        "alipay",
        "taobao",
        "alibaba",
        "alibaba-inc",
        "aliloan",
        "koubei",
        "alitrip",
        "antsdaq",
        "antfortune",
        "ant-open",
        "zmxy",
        "zhimaxy",
        "ant-biz",
        "ssdata",
        "alimama",
      ],
      suffixes: ["com", "net", "cn", "com.cn"],
    },
    { domains: ["alimama", "1688", "alibado", "alisoft"], suffixes: ["cn", "com", "com.cn"] },
    { domains: ["yahoo"], suffixes: ["cn", "com.cn"] },
    { domains: ["zhifubao", "zhifu"], suffixes: ["com"] },
    { domains: ["aliimg"], suffixes: ["com", "net"] },
    { domains: ["alipaydev"], suffixes: ["com"] },
    { domains: ["etao"], suffixes: ["com", "net"] },
    { domains: ["alipayobjects"], suffixes: ["com"] },
    { domains: ["aliexpress"], suffixes: ["com"] },
    { domains: ["aliyun"], suffixes: ["com"] },
    { domains: ["www"], suffixes: ["net.cn"] },
    { domains: ["xin"], suffixes: ["xin"] },
    { domains: ["mybank"], suffixes: ["cn"] },
    { domains: ["mayibank"], suffixes: ["net"] },
    { domains: ["antfin"], suffixes: ["com", "net"] },
  ];
  let pendingAccountInfoRequest = null;
  let cachedAccountInfo = null;
  let cachedAccountInfoAt = 0;
  const userMenuCloseTimers = new WeakMap();
  const clickPinnedUserMenus = new WeakSet();

  function isRecord(value) {
    return Boolean(value && typeof value === "object" && !Array.isArray(value));
  }

  function installAipayApiRuntimeConfig(config = DEFAULT_AIPAY_API_RUNTIME_CONFIG) {
    const existingConfig = isRecord(window.AIPayApiConfig) ? window.AIPayApiConfig : {};
    window.AIPayApiConfig = {
      ...config,
      ...existingConfig,
    };
    return window.AIPayApiConfig;
  }

  function normalizeLogText(value) {
    return String(value ?? "")
      .replace(/\s+/g, " ")
      .trim()
      .slice(0, 200);
  }

  function reportPageExposure(monitor) {
    if (window.__aipayOfficialPageExposureReported) return;
    if (!monitor || typeof monitor.log !== "function") return;

    window.__aipayOfficialPageExposureReported = true;
    try {
      monitor.log({
        code: PAGE_EXPOSURE_CODE,
        msg: "page_exposure",
        d1: normalizeLogText(window.location.pathname || "/"),
        d2: normalizeLogText(document.title || ""),
      });
    } catch {}
  }

  function initPageExposure() {
    if (window.__aipayOfficialPageExposureReported) return;

    if (window.yuyanMonitor && typeof window.yuyanMonitor.log === "function") {
      reportPageExposure(window.yuyanMonitor);
      return;
    }

    if (typeof window.YuyanMonitor === "function") {
      window.yuyanMonitor = new window.YuyanMonitor({
        yuyanId: YUYAN_MONITOR_ID,
      });
      reportPageExposure(window.yuyanMonitor);
      return;
    }

    const script = document.createElement("script");
    script.src = YUYAN_MONITOR_UMD_URL;
    script.crossOrigin = "anonymous";
    script.onload = () => {
      if (typeof window.YuyanMonitor !== "function") return;
      window.yuyanMonitor = new window.YuyanMonitor({
        yuyanId: YUYAN_MONITOR_ID,
      });
      reportPageExposure(window.yuyanMonitor);
    };
    document.head.appendChild(script);
  }

  function normalizeEnv(value) {
    const env = String(value || "").trim().toLowerCase();
    return ["dev", "pre", "prod"].includes(env) ? env : "";
  }

  function normalizeHostname(hostname) {
    return String(hostname || "")
      .trim()
      .toLowerCase()
      .replace(/^\[(.*)\]$/, "$1");
  }

  function normalizeBaseUrl(base) {
    return String(base || "")
      .trim()
      .replace(/\/+$/, "");
  }

  function isTruthyFlag(value) {
    return value === true || value === 1 || String(value || "").trim() === "1";
  }

  function readApiConfig() {
    return isRecord(window.AIPayApiConfig) ? window.AIPayApiConfig : {};
  }

  function hasAccountUserInfo(userInfo) {
    return Boolean(
      userInfo?.userId ||
        userInfo?.customerId ||
        userInfo?.userName ||
        userInfo?.logonName ||
        userInfo?.nickName ||
        userInfo?.name,
    );
  }

  function resolveDisplayName(userInfo) {
    return (
      String(
        userInfo?.userName ||
          userInfo?.logonName ||
          userInfo?.nickName ||
          userInfo?.name ||
          userInfo?.customerId ||
          userInfo?.userId ||
          "开发者",
      ).trim() || "开发者"
    );
  }

  function resolveAvatarUrl(userInfo) {
    return userInfo?.avatarUrl || userInfo?.avatar || userInfo?.headImg || userInfo?.headImgUrl || "";
  }

  function resolveInitial(displayName) {
    const initial = String(displayName || "").replace(/\s+/g, "").charAt(0) || "开";
    return /[a-z]/i.test(initial) ? initial.toUpperCase() : initial;
  }

  function hasSameAccountVisual(previous, next) {
    if (previous?.isLoggedIn !== next?.isLoggedIn) return false;
    if (!next?.isLoggedIn) return true;
    return (
      resolveDisplayName(previous.userInfo) === resolveDisplayName(next.userInfo) &&
      resolveAvatarUrl(previous.userInfo) === resolveAvatarUrl(next.userInfo)
    );
  }

  function readNavAccountCache() {
    try {
      const cached = JSON.parse(window.sessionStorage.getItem(NAV_ACCOUNT_CACHE_KEY) || "null");
      if (
        !isRecord(cached) ||
        cached.version !== NAV_ACCOUNT_CACHE_VERSION ||
        Number(cached.expiresAt || 0) <= Date.now()
      ) {
        window.sessionStorage.removeItem(NAV_ACCOUNT_CACHE_KEY);
        return null;
      }
      return {
        isLoggedIn: cached.isLoggedIn === true,
        userInfo: isRecord(cached.userInfo) ? cached.userInfo : {},
      };
    } catch {
      return null;
    }
  }

  function writeNavAccountCache({ isLoggedIn, userInfo }) {
    try {
      window.sessionStorage.setItem(
        NAV_ACCOUNT_CACHE_KEY,
        JSON.stringify({
          version: NAV_ACCOUNT_CACHE_VERSION,
          expiresAt: Date.now() + NAV_ACCOUNT_CACHE_TTL_MS,
          isLoggedIn: isLoggedIn === true,
          userInfo: isRecord(userInfo) ? userInfo : {},
        }),
      );
    } catch {
      // Storage can be unavailable in privacy-restricted contexts.
    }
  }

  function clearNavAccountCache() {
    try {
      window.sessionStorage.removeItem(NAV_ACCOUNT_CACHE_KEY);
    } catch {
      // Storage can be unavailable in privacy-restricted contexts.
    }
  }

  function inferEnvFromHostname() {
    const hostname = normalizeHostname(window.location.hostname);
    const isIpv4Host = /^(?:\d{1,3}\.){3}\d{1,3}$/.test(hostname)
      ? hostname.split(".").every((part) => {
          const value = Number(part);
          return Number.isInteger(value) && value >= 0 && value <= 255;
        })
      : false;
    const isIpv6Host = hostname.includes(":") && /^[0-9a-f:]+$/i.test(hostname);
    const hasHostLabel = (label) => hostname.split(/[.-]/).includes(label);

    if (
      !hostname ||
      hostname === "localhost" ||
      hostname === "local.dev.alipay.net" ||
      isIpv4Host ||
      isIpv6Host
    ) {
      return "dev";
    }

    if (hasHostLabel("dev") || hasHostLabel("stable")) return "dev";
    if (hasHostLabel("pre")) return "pre";
    return "prod";
  }

  function readQueryEnv() {
    const params = new URLSearchParams(window.location.search);
    for (const key of ["openbridge_env", "aipay_env"]) {
      const env = normalizeEnv(params.get(key));
      if (env) return env;
    }
    return "";
  }

  function readStorageEnv() {
    try {
      return normalizeEnv(window.localStorage?.getItem("aipay:openbridge-env"));
    } catch {
      return "";
    }
  }

  function getOpenBridgeEnv() {
    const existingEnv = normalizeEnv(window.OpenBridge?.env);
    if (existingEnv) return existingEnv;
    const env =
      readQueryEnv() ||
      readStorageEnv() ||
      normalizeEnv(CONFIGURED_OPENBRIDGE_ENV) ||
      inferEnvFromHostname();
    const openBridge = isRecord(window.OpenBridge) ? window.OpenBridge : {};
    openBridge.env = env;
    window.OpenBridge = openBridge;
    return env;
  }

  function installReleaseShellRuntimeConfig() {
    getOpenBridgeEnv();
    installAipayApiRuntimeConfig();
  }

  function isAipayLocalApiProxy() {
    const config = readApiConfig();
    if (
      isTruthyFlag(config.useLocalApiProxy) ||
      isTruthyFlag(config.PUBLIC_AIPAY_USE_LOCAL_API_PROXY)
    ) {
      return true;
    }

    return LOCAL_API_PROXY_HOSTS.has(normalizeHostname(window.location.hostname));
  }

  function getApiBase() {
    const env = getOpenBridgeEnv();
    const config = readApiConfig();

    if (isAipayLocalApiProxy()) return "";

    if (env === "dev") {
      return normalizeBaseUrl(
        config.devWatchtowerOrigin ||
          config.PUBLIC_AIPAY_DEV_WATCHTOWER_ORIGIN ||
          DEFAULT_DEV_WATCHTOWER_ORIGIN,
      );
    }

    return API_BASES[env] || API_BASES.prod;
  }

  function buildApiUrl(pathname) {
    const base = getApiBase();
    if (!base) return pathname;
    return `${base.replace(/\/+$/, "")}/${pathname.replace(/^\/+/, "")}`;
  }

  function shouldUseDevWatchtower() {
    return getOpenBridgeEnv() === "dev" && !isAipayLocalApiProxy();
  }

  function buildApiHeaders(headers) {
    const nextHeaders = new Headers(headers);

    if (shouldUseDevWatchtower()) {
      const config = readApiConfig();
      nextHeaders.set("x-webgw-version", config.webgwVersion || WEBGW_VERSION);
      nextHeaders.set("x-webgw-appid", config.webgwAppId || WEBGW_APP_ID);
      nextHeaders.set(
        WATCHTOWER_PROXY_TARGET_HEADER,
        config.devApiTarget ||
          config.PUBLIC_AIPAY_DEV_API_TARGET ||
          DEFAULT_DEV_API_TARGET,
      );
    }

    return nextHeaders;
  }

  function buildApiRequest(pathname, options = {}) {
    return {
      url: buildApiUrl(pathname),
      headers: buildApiHeaders(options.headers),
    };
  }

  function readOnboardingState() {
    try {
      return JSON.parse(window.localStorage.getItem(ONBOARDING_STORAGE_KEY) || "{}") || {};
    } catch {
      return {};
    }
  }

  function writeLoggedOutOnboardingState() {
    try {
      const currentState = readOnboardingState();
      window.localStorage.setItem(
        ONBOARDING_STORAGE_KEY,
        JSON.stringify({
          ...currentState,
          isLoggedIn: false,
          userInfo: {},
          loginNext: "products",
          pipelineStarting: false,
          qualificationBlocker: null,
        }),
      );
    } catch {
      // 登录态清理失败不阻塞 AuthCenter 登出跳转。
    }
  }

  function hostnameMatchesRule(hostname, domain, suffix) {
    const root = `${domain}.${suffix}`.toLowerCase();
    return hostname === root || hostname.endsWith(`.${root}`);
  }

  function isAllowedLogoutGoto(url) {
    if (url.protocol !== "http:" && url.protocol !== "https:") return false;
    const hostname = url.hostname.toLowerCase();
    return ALLOWED_LOGOUT_GOTO_RULES.some((rule) =>
      rule.domains.some((domain) =>
        rule.suffixes.some((suffix) => hostnameMatchesRule(hostname, domain, suffix)),
      ),
    );
  }

  function buildSafeLogoutReturnUrl(currentHref = window.location.href) {
    const currentUrl = new URL(currentHref, window.location.href);
    currentUrl.searchParams.delete(AUTHCENTER_RETURN_PARAM);
    currentUrl.searchParams.set(AUTHCENTER_RETURN_PARAM, AUTHCENTER_LOGOUT_RETURN_VALUE);
    if (isAllowedLogoutGoto(currentUrl)) return currentUrl.toString();
    return new URL(
      `${currentUrl.pathname}${currentUrl.search}${currentUrl.hash}`,
      LOGOUT_FALLBACK_ORIGIN,
    ).toString();
  }

  function buildAuthCenterLogoutUrl() {
    const config = {
      bizFrom: "alipaysite",
      logoutUrl: "/login/logout.htm",
      ...(window.AIPayAuthCenterConfig || {}),
    };
    const env = getOpenBridgeEnv();
    const origin = String(config.origin || AUTHCENTER_ORIGINS[env] || AUTHCENTER_ORIGINS.prod).replace(
      /\/+$/,
      "",
    );
    const url = new URL(config.logoutUrl || "/login/logout.htm", origin);
    url.searchParams.set("goto", config.logoutReturnUrl || buildSafeLogoutReturnUrl());
    return url.toString();
  }

  function getBridgeUserInfo() {
    const userInfo = window.OpenBridge?.userInfo;
    return isRecord(userInfo) ? userInfo : {};
  }

  function isLoginExpiredResponse(data) {
    if (!isRecord(data)) return false;
    if (String(data.errorCode ?? "") !== LOGIN_EXPIRED_ERROR_CODE) return false;
    return data.success === false || data.isSuccess === false;
  }

  function normalizeAccountInfo(data) {
    const payload = isRecord(data?.data) ? data.data : {};
    const userInfo = isRecord(payload.userInfo) ? payload.userInfo : payload;
    const isLoginExpired = isLoginExpiredResponse(data);
    const loggedInValue =
      typeof payload.loggedIn === "boolean"
        ? payload.loggedIn
        : typeof data?.loggedIn === "boolean"
          ? data.loggedIn
          : undefined;
    const success =
      data?.success === true ||
      data?.isSuccess === true ||
      data?.code === "10000" ||
      loggedInValue === true;
    const isLoggedIn = isLoginExpired
      ? false
      : typeof loggedInValue === "boolean"
        ? loggedInValue
        : Boolean(success && hasAccountUserInfo(userInfo));

    return {
      isLoggedIn,
      isLoginExpired,
      userInfo,
    };
  }

  async function requestAccountInfo() {
    const { url, headers } = buildApiRequest("/login/skillpaycheck.json?_output_charset=utf-8", {
      headers: {
        Accept: "application/json",
      },
    });

    const response = await window.fetch(url, {
      method: "POST",
      credentials: "include",
      headers,
      cache: "no-store",
    });
    if (!response.ok) {
      throw new Error(`请求失败: ${response.status}`);
    }
    return normalizeAccountInfo(await response.json());
  }

  async function requestSkillPaySession() {
    try {
      const { url, headers } = buildApiRequest(SKILLPAY_SESSION_ENDPOINT, {
        headers: { Accept: "application/json" },
      });
      const response = await window.fetch(url, {
        method: "GET",
        credentials: "include",
        cache: "no-store",
        headers,
      });
      if (!response.ok) return { isLoggedIn: false, userInfo: {} };
      const data = await response.json().catch(() => null);
      const payload = isRecord(data?.data) ? data.data : data;
      const userInfo = isRecord(payload?.user) ? payload.user : payload;
      const isLoggedIn = Boolean(
        data?.success === true &&
          isRecord(userInfo) &&
          (userInfo.userId || userInfo.customerId),
      );
      return { isLoggedIn, userInfo: isLoggedIn ? userInfo : {} };
    } catch {
      return { isLoggedIn: false, userInfo: {} };
    }
  }

  function logoutSkillPaySession() {
    const { url, headers } = buildApiRequest(SKILLPAY_LOGOUT_ENDPOINT, {
      headers: { Accept: "application/json" },
    });
    return window.fetch(url, {
      method: "POST",
      credentials: "include",
      cache: "no-store",
      keepalive: true,
      headers,
    }).catch(() => null);
  }

  async function fetchAccountInfo({ force = false } = {}) {
    if (!force && cachedAccountInfo && Date.now() - cachedAccountInfoAt < ACCOUNT_INFO_CACHE_TTL_MS) {
      return cachedAccountInfo;
    }
    if (pendingAccountInfoRequest && !force) return pendingAccountInfoRequest;

    const bridgeUserInfo = getBridgeUserInfo();
    const localState = readOnboardingState();
    const fallback = {
      isLoggedIn: Boolean(localState.isLoggedIn || hasAccountUserInfo(bridgeUserInfo)),
      userInfo: {
        ...(isRecord(localState.userInfo) ? localState.userInfo : {}),
        ...bridgeUserInfo,
      },
    };

    pendingAccountInfoRequest = requestAccountInfo()
      .catch(() => ({ isLoggedIn: false, isLoginExpired: false, userInfo: {} }))
      .then(async (accountInfo) => {
        const alipayAccountInfo = {
          isLoggedIn:
            accountInfo.isLoggedIn || (getOpenBridgeEnv() === "dev" && fallback.isLoggedIn),
          isLoginExpired: accountInfo.isLoginExpired,
          userInfo: {
            ...fallback.userInfo,
            ...accountInfo.userInfo,
          },
        };
        if (alipayAccountInfo.isLoggedIn) return alipayAccountInfo;

        const skillPaySession = await requestSkillPaySession();
        if (!skillPaySession.isLoggedIn) return alipayAccountInfo;
        return {
          isLoggedIn: true,
          isLoginExpired: false,
          userInfo: {
            ...alipayAccountInfo.userInfo,
            ...skillPaySession.userInfo,
          },
        };
      })
      .catch(() => fallback)
      .then((accountInfo) => {
        cachedAccountInfo = accountInfo;
        cachedAccountInfoAt = Date.now();
        return accountInfo;
      })
      .finally(() => {
        pendingAccountInfoRequest = null;
      });

    return pendingAccountInfoRequest;
  }

  function renderAccountState(root, { isLoggedIn, userInfo }) {
    const loginEntry = root.querySelector("[data-nav-login]");
    const consoleEntry = root.querySelector("[data-nav-console]");
    const user = root.querySelector("[data-nav-user]");
    const userName = root.querySelector("[data-nav-user-name]");
    const userInitial = root.querySelector("[data-nav-user-initial]");
    const userAvatarImage = root.querySelector("[data-nav-user-avatar-image]");

    root.toggleAttribute("data-nav-logged-in", isLoggedIn);
    root.dataset.navAccountState = isLoggedIn ? "logged-in" : "logged-out";
    if (loginEntry instanceof HTMLElement) loginEntry.hidden = isLoggedIn;
    if (consoleEntry instanceof HTMLElement) consoleEntry.hidden = !isLoggedIn;
    if (user instanceof HTMLElement) user.hidden = !isLoggedIn;
    if (!isLoggedIn) {
      closeUserMenu(user);
      return;
    }

    const displayName = resolveDisplayName(userInfo);
    if (userName instanceof HTMLElement) userName.textContent = displayName;
    if (userInitial instanceof HTMLElement) userInitial.textContent = resolveInitial(displayName);

    const avatarUrl = resolveAvatarUrl(userInfo);
    if (userAvatarImage instanceof HTMLImageElement) {
      if (!avatarUrl) {
        userAvatarImage.removeAttribute("src");
        userAvatarImage.hidden = true;
        if (userInitial instanceof HTMLElement) userInitial.hidden = false;
        return;
      }

      const revealAvatar = () => {
        userAvatarImage.hidden = false;
        if (userInitial instanceof HTMLElement) userInitial.hidden = true;
      };
      const keepInitial = () => {
        userAvatarImage.hidden = true;
        if (userInitial instanceof HTMLElement) userInitial.hidden = false;
      };
      if (userAvatarImage.getAttribute("src") !== avatarUrl) {
        keepInitial();
        userAvatarImage.src = avatarUrl;
      }
      if (userAvatarImage.complete && userAvatarImage.naturalWidth > 0) {
        revealAvatar();
      } else {
        userAvatarImage.addEventListener("load", revealAvatar, { once: true });
        userAvatarImage.addEventListener("error", keepInitial, { once: true });
      }
    }
  }

  function setUserMenuOpen(user, isOpen) {
    const trigger = user?.querySelector("[data-nav-user-trigger]");
    const menu = user?.querySelector("[data-nav-user-menu]");
    if (!(user instanceof HTMLElement)) return;
    user.classList.toggle("is-open", isOpen);
    if (trigger instanceof HTMLElement) trigger.setAttribute("aria-expanded", String(isOpen));
    if (menu instanceof HTMLElement) menu.setAttribute("aria-hidden", String(!isOpen));
  }

  function clearUserMenuCloseTimer(user) {
    const timer = userMenuCloseTimers.get(user);
    if (timer) {
      window.clearTimeout(timer);
      userMenuCloseTimers.delete(user);
    }
  }

  function openUserMenu(user, { pinned = false } = {}) {
    if (!(user instanceof HTMLElement)) return;
    clearUserMenuCloseTimer(user);
    closeAllUserMenus(user);
    if (pinned) clickPinnedUserMenus.add(user);
    setUserMenuOpen(user, true);
  }

  function closeUserMenu(user) {
    if (!(user instanceof HTMLElement)) return;
    clearUserMenuCloseTimer(user);
    clickPinnedUserMenus.delete(user);
    setUserMenuOpen(user, false);
  }

  function scheduleUserMenuClose(user) {
    if (!(user instanceof HTMLElement) || clickPinnedUserMenus.has(user)) return;
    clearUserMenuCloseTimer(user);
    userMenuCloseTimers.set(
      user,
      window.setTimeout(() => closeUserMenu(user), USER_MENU_CLOSE_DELAY_MS),
    );
  }

  function closeAllUserMenus(exceptUser = null) {
    document.querySelectorAll("[data-nav-user]").forEach((user) => {
      if (user !== exceptUser) closeUserMenu(user);
    });
  }

  function logout(root) {
    void logoutSkillPaySession();
    cachedAccountInfo = null;
    cachedAccountInfoAt = 0;
    pendingAccountInfoRequest = null;
    clearNavAccountCache();
    writeLoggedOutOnboardingState();
    const loginExpiredEvent = new CustomEvent("aipay:login-expired", {
      cancelable: true,
      detail: { resetAuthCenter: true },
    });
    const handledInPlace = !window.dispatchEvent(loginExpiredEvent);
    if (window.AIPayIncentive) window.AIPayIncentive.isLoggedIn = false;
    renderAccountState(root, { isLoggedIn: false, userInfo: {} });
    if (!handledInPlace) window.location.assign(buildAuthCenterLogoutUrl());
  }

  function initLoginEntry(root) {
    const loginEntry = root.querySelector("[data-nav-login]");
    if (loginEntry instanceof HTMLAnchorElement && !loginEntry.getAttribute("href")) {
      loginEntry.href = LOGIN_ENTRY_HREF;
    }
  }

  function syncAllAuthRoots(options = {}) {
    const roots = Array.from(document.querySelectorAll("[data-nav-auth]"));
    if (roots.length === 0) return;
    const cachedAccountInfo = readNavAccountCache();
    if (cachedAccountInfo) {
      const cachedState = cachedAccountInfo.isLoggedIn ? "logged-in" : "logged-out";
      roots.forEach((root) => {
        if (root.dataset.navAccountState !== cachedState) {
          renderAccountState(root, cachedAccountInfo);
        }
      });
    }
    fetchAccountInfo(options).then((accountInfo) => {
      writeNavAccountCache(accountInfo);
      if (
        !options.force &&
        cachedAccountInfo &&
        hasSameAccountVisual(cachedAccountInfo, accountInfo)
      ) {
        return;
      }
      roots.forEach((root) => renderAccountState(root, accountInfo));
    });
  }

  document.querySelectorAll("[data-nav-auth]").forEach((root) => {
    initLoginEntry(root);

    const user = root.querySelector("[data-nav-user]");
    const userTrigger = root.querySelector("[data-nav-user-trigger]");
    const logoutButton = root.querySelector("[data-nav-logout]");

    if (user instanceof HTMLElement) {
      user.addEventListener("pointerenter", () => openUserMenu(user));
      user.addEventListener("pointerleave", () => scheduleUserMenuClose(user));
      user.addEventListener("focusin", () => openUserMenu(user));
      user.addEventListener("focusout", (event) => {
        const nextTarget = event.relatedTarget;
        if (!(nextTarget instanceof Node) || !user.contains(nextTarget)) {
          scheduleUserMenuClose(user);
        }
      });
    }

    if (userTrigger instanceof HTMLElement) {
      userTrigger.addEventListener("click", (event) => {
        event.preventDefault();
        if (!(user instanceof HTMLElement)) return;
        const isPinnedOpen = user.classList.contains("is-open") && clickPinnedUserMenus.has(user);
        if (isPinnedOpen) {
          closeUserMenu(user);
        } else {
          openUserMenu(user, { pinned: true });
        }
      });
    }

    if (logoutButton instanceof HTMLElement) {
      logoutButton.addEventListener("click", (event) => {
        event.preventDefault();
        logout(root);
      });
    }
  });

  installReleaseShellRuntimeConfig();
  initPageExposure();
  syncAllAuthRoots();
  document.addEventListener("click", (event) => {
    const target = event.target instanceof Element ? event.target : null;
    if (target?.closest("[data-nav-user]")) return;
    closeAllUserMenus();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeAllUserMenus();
  });
  window.addEventListener(ACCOUNT_REFRESH_EVENT, () => syncAllAuthRoots({ force: true }));
  window.addEventListener("aipay-onboarding-login-success", () => syncAllAuthRoots({ force: true }));
  window.addEventListener("pageshow", (event) => {
    if (event.persisted) syncAllAuthRoots({ force: true });
  });
})();
