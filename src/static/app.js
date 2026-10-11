const state = {
  token: localStorage.getItem('mshop_token') || '',
  username: localStorage.getItem('mshop_user') || 'Guest',
};

const loginForm = document.querySelector('#login-form');
const signupForm = document.querySelector('#signup-form');
const resetForm = document.querySelector('#reset-form');
const productForm = document.querySelector('#product-form');
const productGrid = document.querySelector('#product-grid');
const shopProductGrid = document.querySelector('#shop-product-grid');
const searchForm = document.querySelector('#header-search-form');
const searchInput = document.querySelector('#product-search-input');
const brandHomeButton = document.querySelector('#brand-home-button');
const authStatus = document.querySelector('#auth-status');
const productStatus = document.querySelector('#product-status');
const logoutButton = document.querySelector('#logout-button');
const accountButton = document.querySelector('#account-button');
const newProductHeaderButton = document.querySelector('#new-product-header');
const loginOpenButton = document.querySelector('#login-open');
const signupOpenButton = document.querySelector('#signup-open');
const refreshButton = document.querySelector('#refresh-products');
const refreshButtonShop = document.querySelector('#refresh-products-shop');
const categoryButtons = document.querySelectorAll('.market-chip');
const tabButtons = document.querySelectorAll('.tab-button');
const tabTriggers = document.querySelectorAll('.tab-trigger');
const panels = document.querySelectorAll('.tab-panel');
const authModal = document.querySelector('#auth-modal');
const authTabs = document.querySelectorAll('.auth-tab');
const authForms = document.querySelectorAll('.auth-form');
const accountDashboard = document.querySelector('#account-dashboard');
const accountLogoutButton = document.querySelector('#account-logout');
const accountViewButtons = document.querySelectorAll('.account-nav');
const accountViews = document.querySelectorAll('.account-view');
const accountProductForm = document.querySelector('#account-product-form');
const accountProductStatus = document.querySelector('#account-product-status');
const productDetailModal = document.querySelector('#product-detail-modal');
const productDetailContent = document.querySelector('#product-detail-content');
const toastContainer = document.querySelector('#toast-container');
const sellerNameCache = new Map();

function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function setStatus(element, message, type = '') {
  if (!element) {
    return;
  }

  element.textContent = message;
  element.classList.remove('success', 'error');
  if (type) {
    element.classList.add(type);
  }
}

function showToast(message, type = 'success') {
  if (!toastContainer) {
    return;
  }

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.textContent = message;
  toastContainer.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, 3200);
}

function normalizeValidationMessage(message) {
  if (!message) {
    return 'Something went wrong.';
  }

  return String(message)
    .replace(/^Value error,\s*/i, '')
    .replace(/^Validation error,\s*/i, '')
    .replace(/^Field required\s*/i, 'This field is required')
    .trim();
}

function getErrorMessage(error, fallback = 'Something went wrong.') {
  if (error && error.message) {
    return normalizeValidationMessage(error.message);
  }

  return fallback;
}

function extractApiErrorMessage(payload, fallback = 'Request failed') {
  if (!payload) {
    return fallback;
  }

  if (typeof payload === 'string') {
    return normalizeValidationMessage(payload);
  }

  if (payload.detail) {
    if (Array.isArray(payload.detail)) {
      const first = payload.detail[0];
      if (first && typeof first === 'object') {
        return normalizeValidationMessage(first.msg || first.error || first.message || fallback);
      }
      return normalizeValidationMessage(String(first || fallback));
    }

    if (typeof payload.detail === 'object') {
      return normalizeValidationMessage(payload.detail.msg || payload.detail.error || payload.detail.message || fallback);
    }

    return normalizeValidationMessage(payload.detail);
  }

  if (payload.message) {
    return normalizeValidationMessage(payload.message);
  }

  return fallback;
}

function validatePasswordStrength(password) {
  const errors = [];

  if (!password) {
    return ['Password is required.'];
  }

  if (password.length < 8) {
    errors.push('Password must be at least 8 characters long.');
  }

  if (!/[A-Z]/.test(password)) {
    errors.push('Password must contain at least 1 uppercase letter.');
  }

  if (!/[a-z]/.test(password)) {
    errors.push('Password must contain at least 1 lowercase letter.');
  }

  if (!/\d/.test(password)) {
    errors.push('Password must contain at least 1 number.');
  }

  return errors;
}

function selectTab(tabName) {
  const visibleTabButtons = document.querySelectorAll('.tab-button');
  visibleTabButtons.forEach((button) => {
    button.classList.toggle('active', button.dataset.tab === tabName);
  });

  panels.forEach((panel) => {
    panel.classList.toggle('active', panel.id === `${tabName}-panel`);
  });
}

function setAuthForm(mode) {
  authTabs.forEach((button) => {
    button.classList.toggle('active', button.dataset.authMode === mode);
  });

  authForms.forEach((form) => {
    const isVisible = form.id === `${mode}-form`;
    form.classList.toggle('active', isVisible);
  });

  const titleMap = {
    login: 'Sign in',
    signup: 'Create account',
    reset: 'Reset password',
  };

  const titleEl = document.querySelector('#auth-modal-title');
  if (titleEl) {
    titleEl.textContent = titleMap[mode] || 'Sign in';
  }
}

function openAuthModal(mode = 'login') {
  if (!authModal) {
    return;
  }

  authModal.classList.remove('hidden');
  authModal.setAttribute('aria-hidden', 'false');
  setAuthForm(mode);
  setStatus(authStatus, '', '');
}

function closeAuthModal() {
  if (!authModal) {
    return;
  }

  authModal.classList.add('hidden');
  authModal.setAttribute('aria-hidden', 'true');
  setStatus(authStatus, '', '');
}

function setAccountView(viewName) {
  accountViewButtons.forEach((button) => {
    button.classList.toggle('active', button.dataset.accountView === viewName);
  });

  accountViews.forEach((view) => {
    view.classList.toggle('active', view.dataset.accountView === viewName);
  });
}

function renderAccountDashboard() {
  if (!accountDashboard) {
    return;
  }

  const isLoggedIn = Boolean(state.token);

  if (!isLoggedIn) {
    accountDashboard.innerHTML = '<div class="account-skeleton"><p>Please sign in to see your dashboard.</p></div>';
    return;
  }

  const userLabel = escapeHtml(state.username || 'Seller');

  const accountName = document.querySelector('[data-account-view="profile"] strong');
  if (accountName) {
    accountName.textContent = userLabel;
  }

  const productCount = document.querySelector('[data-account-view="profile"] .account-card:nth-child(2) strong');
  if (productCount) {
    productCount.textContent = '0';
  }

  const viewCount = document.querySelector('[data-account-view="profile"] .account-card:nth-child(3) strong');
  if (viewCount) {
    viewCount.textContent = '0';
  }

  const profileText = document.querySelector('[data-account-view="profile"] .account-list li');
  if (profileText) {
    profileText.textContent = `Username: ${userLabel}`;
  }
}

function setAuthState() {
  const isLoggedIn = Boolean(state.token);
  const productSubmitButton = document.querySelector('#product-form button[type="submit"]');

  if (loginOpenButton) {
    loginOpenButton.classList.toggle('hidden', isLoggedIn);
  }

  if (signupOpenButton) {
    signupOpenButton.classList.toggle('hidden', isLoggedIn);
  }

  if (logoutButton) {
    logoutButton.classList.toggle('hidden', !isLoggedIn);
  }

  if (accountButton) {
    accountButton.classList.toggle('hidden', !isLoggedIn);
    accountButton.textContent = isLoggedIn ? `${state.username || 'My'} account` : 'My account';
  }

  if (newProductHeaderButton) {
    newProductHeaderButton.classList.toggle('hidden', !isLoggedIn);
  }

  if (productSubmitButton) {
    productSubmitButton.disabled = !isLoggedIn;
    productSubmitButton.title = isLoggedIn ? 'Add product' : 'Log in to add products';
  }

  renderAccountDashboard();

  if (!isLoggedIn) {
    setStatus(authStatus, 'Log in to browse products and create listings.', '');
    if (productStatus) {
      setStatus(productStatus, 'Please sign in before creating a product.', 'error');
    }
  }
}

async function apiRequest(url, options = {}) {
  const headers = {
    ...(options.headers || {}),
  };

  if (!(options.body instanceof FormData) && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json';
  }

  if (state.token) {
    headers.Authorization = `Bearer ${state.token}`;
  }

  const response = await fetch(url, {
    ...options,
    headers,
  });

  const contentType = response.headers.get('content-type') || '';
  const body = contentType.includes('application/json')
    ? await response.json()
    : await response.text();

  if (!response.ok) {
    const message = extractApiErrorMessage(body, 'Request failed');
    throw new Error(message);
  }

  return body;
}

function getFilteredProducts(items) {
  const query = (searchInput?.value || '').trim().toLowerCase();
  const selectedCategory = document.querySelector('.market-chip.active')?.dataset.category || 'All';

  return items.filter((product) => {
    const matchesCategory = selectedCategory === 'All' || product.category_name === selectedCategory;
    const haystack = [
      product.name,
      product.description,
      product.category_name,
    ]
      .filter(Boolean)
      .join(' ')
      .toLowerCase();
    const matchesSearch = !query || haystack.includes(query);

    return matchesCategory && matchesSearch;
  });
}

async function getSellerName(userId) {
  if (!userId) {
    return 'Unknown seller';
  }

  if (sellerNameCache.has(userId)) {
    return sellerNameCache.get(userId);
  }

  try {
    const user = await apiRequest(`/api/v1/auth/user/${userId}`);
    const username = user?.username || `Seller #${userId}`;
    sellerNameCache.set(userId, username);
    return username;
  } catch (error) {
    const fallback = `Seller #${userId}`;
    sellerNameCache.set(userId, fallback);
    return fallback;
  }
}

function renderProducts(items, targetGrid) {
  if (!targetGrid) {
    return;
  }

  const filtered = getFilteredProducts(items);

  if (!filtered.length) {
    targetGrid.innerHTML = '<div class="empty-state">No matching products found.</div>';
    return;
  }

  targetGrid.innerHTML = filtered
    .map(
      (product) => `
        <button type="button" class="product-card product-clickable" data-product-id="${escapeHtml(product.id)}" aria-label="Open ${escapeHtml(product.name || 'product')}">
          <div class="product-image" aria-hidden="true"></div>
          <h3>${escapeHtml(product.name || 'Untitled item')}</h3>
          <p>${escapeHtml(product.description || 'No description provided.')}</p>
          <div class="meta-row">
            <span>${escapeHtml(product.category_name || 'Other')}</span>
            <span>Qty: ${escapeHtml(product.quantity || 0)}</span>
          </div>
          <div class="product-price">€${Number(product.price || 0).toFixed(2)}</div>
          <div class="meta-row">
            <span>ID: ${escapeHtml(product.id || 'n/a')}</span>
            <span>Seller: ${escapeHtml(product.seller_name || 'Loading...')}</span>
          </div>
        </button>
      `
    )
    .join('');

  targetGrid.querySelectorAll('.product-card').forEach((card) => {
    card.addEventListener('click', async () => {
      const productId = card.dataset.productId;
      if (!productId) {
        return;
      }

      await openProductDetail(Number(productId));
    });

    card.addEventListener('keydown', async (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        const productId = card.dataset.productId;
        if (productId) {
          await openProductDetail(Number(productId));
        }
      }
    });
  });
}

async function openProductDetail(productId) {
  if (!productDetailModal || !productDetailContent) {
    return;
  }

  try {
    const product = await apiRequest(`/api/v1/products/${productId}`);
    const sellerName = await getSellerName(product.user_id);

    productDetailContent.innerHTML = `
      <div class="detail-header">
        <p class="eyebrow accent">Listing details</p>
        <h2 id="product-detail-title">${escapeHtml(product.name || 'Untitled item')}</h2>
      </div>
      <div class="product-image detail-image" aria-hidden="true"></div>
      <div class="detail-grid">
        <div class="detail-stat">
          <span>Price</span>
          <strong>€${Number(product.price || 0).toFixed(2)}</strong>
        </div>
        <div class="detail-stat">
          <span>Quantity</span>
          <strong>${escapeHtml(product.quantity || 0)}</strong>
        </div>
      </div>
      <div class="detail-block">
        <h3>Description</h3>
        <p>${escapeHtml(product.description || 'No description provided.')}</p>
      </div>
      <div class="detail-block">
        <h3>Seller</h3>
        <p><strong>Username:</strong> ${escapeHtml(sellerName)}</p>
        <p><strong>Seller ID:</strong> ${escapeHtml(product.user_id)}</p>
        <p><strong>Category:</strong> ${escapeHtml(product.category_name || 'Other')}</p>
      </div>
    `;

    productDetailModal.classList.remove('hidden');
    productDetailModal.setAttribute('aria-hidden', 'false');
  } catch (error) {
    showToast(getErrorMessage(error, 'Unable to open product details'), 'error');
  }
}

async function loadProducts() {
  try {
    const payload = await apiRequest('/api/v1/products/products?page=1&size=20');
    const items = payload.items || [];
    const enrichedItems = await Promise.all(
      items.map(async (product) => ({
        ...product,
        seller_name: await getSellerName(product.user_id),
      }))
    );
    renderProducts(enrichedItems, productGrid);
    renderProducts(enrichedItems, shopProductGrid);
  } catch (error) {
    const fallback = '<div class="empty-state">Unable to load products right now.</div>';
    if (productGrid) {
      productGrid.innerHTML = fallback;
    }
    if (shopProductGrid) {
      shopProductGrid.innerHTML = fallback;
    }
    setStatus(productStatus, error.message, 'error');
  }
}

async function loginUser(event) {
  event.preventDefault();
  const formData = new FormData(loginForm);
  const username = formData.get('username');
  const password = formData.get('password');

  try {
    const response = await fetch('/api/v1/auth/login/new/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({ username, password }),
    });

    let body = null;
    try {
      body = await response.json();
    } catch {
      body = null;
    }

    if (!response.ok) {
      const errorMessage = extractApiErrorMessage(body, 'Incorrect credentials');
      throw new Error(errorMessage);
    }

    state.token = body.access_token;
    state.username = username;
    localStorage.setItem('mshop_token', state.token);
    localStorage.setItem('mshop_user', state.username);

    setStatus(authStatus, `Signed in as ${username}.`, 'success');
    showToast('Signed in successfully', 'success');
    closeAuthModal();
    setAuthState();
    await loadProducts();
    selectTab('account');
    loginForm.reset();
  } catch (error) {
    const message = getErrorMessage(error, 'Incorrect credentials');
    setStatus(authStatus, message, 'error');
    showToast(message, 'error');
  }
}

async function createUser(event) {
  event.preventDefault();
  const formData = new FormData(signupForm);

  const payload = {
    username: formData.get('signup-username'),
    email: formData.get('signup-email'),
    password: formData.get('signup-password'),
  };

  const passwordErrors = validatePasswordStrength(String(payload.password || ''));
  if (passwordErrors.length > 0) {
    const message = passwordErrors[0];
    setStatus(authStatus, message, 'error');
    showToast(message, 'error');
    return;
  }

  try {
    await apiRequest('/api/v1/auth/signIn', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    setStatus(authStatus, 'Account created successfully. You can sign in now.', 'success');
    showToast('Account created successfully', 'success');
    signupForm.reset();
    setAuthForm('login');
  } catch (error) {
    const message = getErrorMessage(error, 'Unable to create account.');
    setStatus(authStatus, message, 'error');
    showToast(message, 'error');
  }
}

async function resetPassword(event) {
  event.preventDefault();
  const formData = new FormData(resetForm);
  const email = formData.get('reset-email');

  if (!email) {
    setStatus(authStatus, 'Please enter your email address.', 'error');
    return;
  }

  setStatus(authStatus, `Password reset instructions sent to ${email}.`, 'success');
  showToast('Reset link sent', 'success');
  resetForm.reset();
  setAuthForm('login');
}

async function createProduct(event) {
  event.preventDefault();

  if (!state.token) {
    setStatus(productStatus, 'Please sign in before creating a product.', 'error');
    showToast('Please sign in before creating a product.', 'error');
    return;
  }

  const formData = new FormData(event.target);
  const payload = {
    name: formData.get('name') || formData.get('account-name'),
    description: formData.get('description') || formData.get('account-description') || '',
    price: Number(formData.get('price') || formData.get('account-price')),
    quantity: Number(formData.get('quantity') || formData.get('account-quantity')),
    category_name: formData.get('category_name') || formData.get('account-category') || 'Other',
  };

  try {
    await apiRequest('/api/v1/products/new', {
      method: 'POST',
      body: JSON.stringify(payload),
    });

    const statusTarget = event.target === accountProductForm ? accountProductStatus : productStatus;
    setStatus(statusTarget, 'Product created successfully.', 'success');
    showToast('Product created successfully', 'success');
    event.target.reset();
    await loadProducts();
    setAccountView('products');
    selectTab('shop');
  } catch (error) {
    const message = getErrorMessage(error, 'Unable to create product.');
    const statusTarget = event.target === accountProductForm ? accountProductStatus : productStatus;
    setStatus(statusTarget, message, 'error');
    showToast(message, 'error');
  }
}

function closeProductDetailModal() {
  if (!productDetailModal) {
    return;
  }

  productDetailModal.classList.add('hidden');
  productDetailModal.setAttribute('aria-hidden', 'true');
}

function logout() {
  state.token = '';
  state.username = 'Guest';
  localStorage.removeItem('mshop_token');
  localStorage.removeItem('mshop_user');
  setStatus(authStatus, 'You have been logged out.', '');
  showToast('You have been logged out', 'success');
  setAuthState();
  selectTab('home');
}

function handleProductSearch() {
  const query = (searchInput?.value || '').trim();
  if (query) {
    selectTab('home');
  }

  if (searchInput) {
    searchInput.value = query;
  }

  loadProducts();
}

function setCategoryFilter(categoryName) {
  categoryButtons.forEach((button) => {
    button.classList.toggle('active', button.dataset.category === categoryName);
  });

  if (searchInput && !(searchInput.value || '').trim()) {
    selectTab('home');
  }

  loadProducts();
}

function bindAuthTabs() {
  authTabs.forEach((button) => {
    button.addEventListener('click', () => setAuthForm(button.dataset.authMode));
  });

  document.querySelectorAll('.password-reset-trigger').forEach((button) => {
    button.addEventListener('click', () => setAuthForm('reset'));
  });

  document.querySelectorAll('[data-close-modal="true"]').forEach((button) => {
    button.addEventListener('click', closeAuthModal);
  });

  document.querySelectorAll('[data-product-close-modal="true"]').forEach((button) => {
    button.addEventListener('click', closeProductDetailModal);
  });

  document.querySelector('.modal-close')?.addEventListener('click', closeAuthModal);
  document.querySelector('.product-modal-close')?.addEventListener('click', closeProductDetailModal);
}

brandHomeButton?.addEventListener('click', () => {
  selectTab('home');
  searchInput?.focus();
});

tabButtons.forEach((button) => {
  button.addEventListener('click', () => selectTab(button.dataset.tab));
});

categoryButtons.forEach((button) => {
  button.addEventListener('click', () => setCategoryFilter(button.dataset.category));
});

tabTriggers.forEach((button) => {
  button.addEventListener('click', () => selectTab(button.dataset.tab));
});

loginForm.addEventListener('submit', loginUser);
signupForm.addEventListener('submit', createUser);
resetForm.addEventListener('submit', resetPassword);
productForm.addEventListener('submit', createProduct);
accountProductForm.addEventListener('submit', createProduct);
logoutButton.addEventListener('click', logout);
accountLogoutButton.addEventListener('click', logout);
loginOpenButton.addEventListener('click', () => openAuthModal('login'));
signupOpenButton.addEventListener('click', () => openAuthModal('signup'));
newProductHeaderButton.addEventListener('click', () => {
  setAccountView('new-product');
  selectTab('account');
});
accountButton.addEventListener('click', () => {
  setAccountView('profile');
  selectTab('account');
});
accountViewButtons.forEach((button) => {
  button.addEventListener('click', () => setAccountView(button.dataset.accountView));
});
refreshButton.addEventListener('click', loadProducts);
refreshButtonShop.addEventListener('click', loadProducts);

if (searchInput) {
  searchInput.addEventListener('input', () => {
    if ((searchInput.value || '').trim()) {
      selectTab('home');
    }
    loadProducts();
  });

  searchInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      handleProductSearch();
    }
  });
}

searchForm?.addEventListener('submit', (event) => {
  event.preventDefault();
  handleProductSearch();
});

bindAuthTabs();
setAuthState();
setAccountView('profile');
selectTab('home');
loadProducts();
