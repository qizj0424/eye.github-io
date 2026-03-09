// ==================== 配置 ====================
const GITHUB_CONFIG = {
    owner: 'qizj0424',
    repo: 'eye.github-io',
    path: 'data/menus.json',
    branch: 'main',
    token: ''
};

const FOOD_ICONS = ['🍖', '🥩', '🍗', '🥘', '🍲', '🥗', '🍜', '🍝', '🍛', '🍤', '🥟', '🍳', '🥦', '🍅', '🐟'];

// ==================== 状态管理 ====================
const state = {
    menus: [],
    githubToken: GITHUB_CONFIG.token || localStorage.getItem('githubToken') || '',
    currentView: localStorage.getItem('menuViewMode') || 'grid',
    fileSha: '',
    isLoading: false
};

// ==================== 默认数据 ====================
const defaultMenus = [
    {
        id: 1,
        name: '红烧肉',
        desc: '肥而不腻，入口即化的经典家常菜',
        tags: ['家常菜', '下饭菜', '经典'],
        icon: '🥩',
        ingredients: ['五花肉 500克', '生姜 3片', '大葱 1根', '冰糖 30克', '生抽 2勺', '老抽 1勺', '料酒 2勺', '八角 2个'],
        steps: ['五花肉洗净切成3厘米见方的块', '冷水下锅，加入料酒和姜片焯水去腥', '捞出沥干，锅中放少许油，小火炒糖色', '糖色呈琥珀色时，放入肉块翻炒均匀', '加入生抽、老抽、八角和适量开水', '大火烧开后转小火炖煮45分钟', '大火收汁，汤汁浓稠即可出锅']
    },
    {
        id: 2,
        name: '番茄炒蛋',
        desc: '酸甜可口，营养均衡的快手菜',
        tags: ['快手菜', '素食', '家常菜'],
        icon: '🍅',
        ingredients: ['番茄 2个', '鸡蛋 3个', '葱花 适量', '盐 1勺', '糖 1勺', '食用油 适量'],
        steps: ['番茄洗净切块，鸡蛋打散备用', '热锅凉油，倒入蛋液炒至凝固盛出', '锅中再加少许油，放入番茄翻炒出汁', '加入炒好的鸡蛋一起翻炒', '调入盐和糖，撒上葱花即可出锅']
    },
    {
        id: 3,
        name: '麻婆豆腐',
        desc: '麻辣鲜香，川菜经典代表',
        tags: ['川菜', '辣', '下饭菜'],
        icon: '🌶️',
        ingredients: ['嫩豆腐 400克', '猪肉末 100克', '豆瓣酱 2勺', '花椒粉 1勺', '蒜末 适量', '姜末 适量', '葱花 适量', '水淀粉 适量'],
        steps: ['豆腐切成2厘米见方的块，用开水焯烫去豆腥味', '锅中放油，下肉末炒至变色', '加入豆瓣酱、蒜末、姜末炒出红油', '加入适量水烧开，放入豆腐', '中小火烧3-5分钟让豆腐入味', '淋入水淀粉勾芡，撒上花椒粉和葱花即可']
    },
    {
        id: 4,
        name: '清蒸鲈鱼',
        desc: '鲜美嫩滑，保留鱼肉原味',
        tags: ['粤菜', '清淡', '海鲜'],
        icon: '🐟',
        ingredients: ['鲈鱼 1条（约500克）', '姜丝 适量', '葱丝 适量', '蒸鱼豉油 3勺', '料酒 1勺', '食用油 适量'],
        steps: ['鲈鱼处理干净，两面划几刀便于入味', '鱼身抹上料酒，铺上姜丝腌制10分钟', '水烧开后放入鱼，大火蒸8-10分钟', '取出倒掉蒸出的汤汁，铺上葱丝', '淋上蒸鱼豉油，热油浇在葱丝上即可']
    },
    {
        id: 5,
        name: '糖醋排骨',
        desc: '酸甜开胃，老少皆宜',
        tags: ['家常菜', '下饭菜', '甜酸'],
        icon: '🍖',
        ingredients: ['猪小排 500克', '冰糖 30克', '米醋 3勺', '生抽 2勺', '料酒 1勺', '白芝麻 适量', '姜片 3片'],
        steps: ['排骨斩块，冷水下锅焯水去血沫', '捞出洗净沥干备用', '锅中放油和冰糖，小火炒至糖色', '放入排骨翻炒上色', '加入生抽、米醋、料酒和适量水', '大火烧开后转小火炖煮30分钟', '大火收汁，撒白芝麻出锅']
    },
    {
        id: 6,
        name: '蒜蓉西兰花',
        desc: '清爽脆嫩，营养丰富',
        tags: ['素食', '快手菜', '健康'],
        icon: '🥦',
        ingredients: ['西兰花 1颗', '大蒜 5瓣', '盐 1勺', '蚝油 1勺', '食用油 适量'],
        steps: ['西兰花切小朵，用盐水浸泡10分钟后洗净', '大蒜切成蒜蓉', '烧一锅水，加少许盐和油，放入西兰花焯烫1分钟', '捞出过凉水，保持翠绿色泽', '热锅凉油，小火炒香蒜蓉', '放入西兰花，加入蚝油和盐快速翻炒均匀即可']
    }
];

// ==================== DOM 元素缓存 ====================
const elements = {};

function cacheElements() {
    const ids = ['homePage', 'detailPage', 'menuGrid', 'emptyState', 'listTitle', 'searchInput',
                 'uploadModal', 'tokenModal', 'modalTitle', 'submitBtn', 'editMenuId',
                 'menuName', 'menuDesc', 'menuTags', 'menuIngredients', 'menuSteps',
                 'githubToken', 'gridViewBtn', 'listViewBtn', 'toast', 'detailContent', 'tokenBtn'];
    ids.forEach(id => elements[id] = document.getElementById(id));
}

// ==================== 工具函数 ====================
const utils = {
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },

    debounce(fn, delay) {
        let timer = null;
        return function(...args) {
            clearTimeout(timer);
            timer = setTimeout(() => fn.apply(this, args), delay);
        };
    },

    getRandomIcon() {
        return FOOD_ICONS[Math.floor(Math.random() * FOOD_ICONS.length)];
    },

    parseTags(tagsStr) {
        return tagsStr ? tagsStr.split(/[,，]/).map(t => t.trim()).filter(Boolean) : ['未分类'];
    },

    parseList(text) {
        return text.split('\n').map(l => l.trim()).filter(Boolean);
    },

    // UTF-8 安全的 Base64 编码（支持中文）
    utf8ToBase64(str) {
        const bytes = new TextEncoder().encode(str);
        const binString = Array.from(bytes, (b) => String.fromCharCode(b)).join('');
        return btoa(binString);
    },

    // UTF-8 安全的 Base64 解码（支持中文）
    base64ToUtf8(base64) {
        const binString = atob(base64);
        const bytes = Uint8Array.from(binString, (c) => c.charCodeAt(0));
        return new TextDecoder().decode(bytes);
    }
};

// ==================== UI 函数 ====================
function showToast(message, duration = 3000) {
    elements.toast.textContent = message;
    elements.toast.classList.add('show');
    setTimeout(() => elements.toast.classList.remove('show'), duration);
}

function setLoading(loading) {
    state.isLoading = loading;
    document.body.style.cursor = loading ? 'wait' : '';
}

// ==================== GitHub API ====================
const github = {
    get baseUrl() {
        return `https://api.github.com/repos/${GITHUB_CONFIG.owner}/${GITHUB_CONFIG.repo}/contents/${GITHUB_CONFIG.path}`;
    },

    getHeaders() {
        return {
            'Authorization': `token ${state.githubToken}`,
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        };
    },

    async load() {
        if (!state.githubToken) {
            showTokenModal();
            return false;
        }

        setLoading(true);
        try {
            showToast('📡 正在加载数据...');
            const response = await fetch(`${this.baseUrl}?ref=${GITHUB_CONFIG.branch}`, {
                headers: this.getHeaders()
            });

            if (response.status === 404) {
                state.menus = [...defaultMenus];
                return await this.save('创建初始菜单数据');
            }

            if (!response.ok) {
                if (response.status === 401) {
                    showToast('❌ Token 无效或已过期');
                    showTokenModal();
                    return false;
                }
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            state.fileSha = data.sha;
            const content = utils.base64ToUtf8(data.content.replace(/\n/g, ''));
            const parsed = JSON.parse(content);
            state.menus = parsed?.length ? parsed : [...defaultMenus];
            showToast('✅ 数据加载成功！');
            return true;
        } catch (error) {
            console.error('加载失败:', error);
            showToast('❌ 加载失败，使用默认数据');
            state.menus = [...defaultMenus];
            return true;
        } finally {
            setLoading(false);
        }
    },

    async save(message = '更新菜单数据') {
        if (!state.githubToken) {
            showTokenModal();
            return false;
        }

        setLoading(true);
        try {
            showToast('💾 正在保存...');
            const content = utils.utf8ToBase64(JSON.stringify(state.menus, null, 2));
            const body = { message, content, branch: GITHUB_CONFIG.branch };
            if (state.fileSha) body.sha = state.fileSha;

            const response = await fetch(this.baseUrl, {
                method: 'PUT',
                headers: this.getHeaders(),
                body: JSON.stringify(body)
            });

            if (!response.ok) {
                if (response.status === 401) {
                    showToast('❌ Token 无效或已过期');
                    showTokenModal();
                    return false;
                }
                if (response.status === 409) {
                    showToast('⚠️ 数据冲突，正在重新加载...');
                    return await this.load();
                }
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            state.fileSha = data.content.sha;
            showToast('✅ 保存成功！');
            return true;
        } catch (error) {
            console.error('保存失败:', error);
            showToast('❌ 保存失败: ' + error.message);
            return false;
        } finally {
            setLoading(false);
        }
    }
};

// ==================== 渲染函数 ====================
function renderMenus(menuList = state.menus, title = `全部菜单 (${state.menus.length})`) {
    elements.listTitle.textContent = title;

    // 应用视图样式
    const container = elements.menuGrid;
    container.className = state.currentView === 'list' ? 'menu-list' : 'menu-grid';

    if (!menuList.length) {
        container.innerHTML = '';
        elements.emptyState.style.display = 'block';
        return;
    }

    elements.emptyState.style.display = 'none';
    container.innerHTML = menuList.map(menu => createMenuCard(menu)).join('');
}

function createMenuCard(menu) {
    const escapedName = utils.escapeHtml(menu.name);
    const escapedDesc = utils.escapeHtml(menu.desc || '暂无描述');
    const tagsHtml = menu.tags.map(tag => `<span class="tag">${utils.escapeHtml(tag)}</span>`).join('');

    return `
        <div class="menu-card" style="animation-delay: ${Math.random() * 0.2}s">
            <div class="card-actions">
                <button class="card-btn edit" onclick="event.stopPropagation(); openEditModal(${menu.id})" title="编辑">✏️</button>
                <button class="card-btn delete" onclick="event.stopPropagation(); deleteMenu(${menu.id})" title="删除">🗑️</button>
            </div>
            <div class="menu-card-main" onclick="showDetail(${menu.id})">
                <div class="menu-image">${menu.icon}</div>
                <div class="menu-content">
                    <h3 class="menu-title">${escapedName}</h3>
                    <p class="menu-desc">${escapedDesc}</p>
                    <div class="menu-tags">${tagsHtml}</div>
                </div>
            </div>
        </div>
    `;
}

function renderDetail(menu) {
    const tagsHtml = menu.tags.map(tag => `<span class="tag">${utils.escapeHtml(tag)}</span>`).join('');
    const ingredientsHtml = menu.ingredients.map(ing =>
        `<div class="ingredient-item">${utils.escapeHtml(ing)}</div>`
    ).join('');
    const stepsHtml = menu.steps.map((step, i) => `
        <div class="step-item">
            <div class="step-number">${i + 1}</div>
            <div class="step-content">${utils.escapeHtml(step)}</div>
        </div>
    `).join('');

    elements.detailContent.innerHTML = `
        <div class="detail-hero">
            <div class="detail-icon">${menu.icon}</div>
            <h1 class="detail-title">${utils.escapeHtml(menu.name)}</h1>
            <p class="detail-desc">${utils.escapeHtml(menu.desc || '暂无描述')}</p>
            <div class="menu-tags" style="justify-content: center; margin-top: 16px;">${tagsHtml}</div>
            <div style="margin-top: 20px; display: flex; gap: 12px; justify-content: center;">
                <button class="btn btn-secondary" onclick="openEditModal(${menu.id})">✏️ 编辑菜单</button>
                <button class="btn btn-outline" onclick="deleteMenu(${menu.id}, true)" style="border-color: #ff6b6b; color: #ff6b6b;">🗑️ 删除菜单</button>
            </div>
        </div>
        <div class="detail-section">
            <h3>🥬 所需食材</h3>
            <div class="ingredients-list">${ingredientsHtml}</div>
        </div>
        <div class="detail-section">
            <h3>👨‍🍳 制作步骤</h3>
            <div class="steps-list">${stepsHtml}</div>
        </div>
    `;
}

// ==================== 视图控制 ====================
function switchView(view) {
    state.currentView = view;
    localStorage.setItem('menuViewMode', view);
    elements.gridViewBtn.classList.toggle('active', view === 'grid');
    elements.listViewBtn.classList.toggle('active', view === 'list');

    // 根据当前状态重新渲染
    const keyword = elements.searchInput.value.trim();
    const title = elements.listTitle.textContent;

    if (keyword) {
        searchMenus();
    } else if (title.includes('随机推荐')) {
        generateRandomMenus();
    } else {
        renderMenus();
    }
}

function showDetail(id) {
    const menu = state.menus.find(m => m.id === id);
    if (!menu) return;

    renderDetail(menu);
    elements.homePage.classList.add('hidden');
    elements.detailPage.classList.add('active');
    window.scrollTo(0, 0);
}

function backToHome() {
    elements.detailPage.classList.remove('active');
    elements.homePage.classList.remove('hidden');
}

// ==================== 搜索功能 ====================
function searchMenus() {
    const keyword = elements.searchInput.value.trim().toLowerCase();
    if (!keyword) {
        showAllMenus();
        return;
    }

    const results = state.menus.filter(menu =>
        menu.name.toLowerCase().includes(keyword) ||
        (menu.desc && menu.desc.toLowerCase().includes(keyword)) ||
        menu.ingredients.some(i => i.toLowerCase().includes(keyword)) ||
        menu.tags.some(t => t.toLowerCase().includes(keyword))
    );

    renderMenus(results, `搜索结果: "${keyword}" (${results.length})`);
}

function showAllMenus() {
    elements.searchInput.value = '';
    renderMenus();
}

function generateRandomMenus() {
    const count = Math.min(parseInt(document.getElementById('randomCount').value) || 3, state.menus.length);
    const shuffled = [...state.menus].sort(() => Math.random() - 0.5);
    const randomMenus = shuffled.slice(0, count);
    renderMenus(randomMenus, `🎲 随机推荐 (${randomMenus.length})`);
    showToast(`已为您随机生成 ${count} 道菜品`);
}

// ==================== 模态框控制 ====================
function openUploadModal() {
    elements.modalTitle.textContent = '📝 上传新菜单';
    elements.submitBtn.textContent = '✅ 保存菜单';
    elements.editMenuId.value = '';
    document.getElementById('uploadForm').reset();
    elements.uploadModal.classList.add('active');
}

function openEditModal(id) {
    const menu = state.menus.find(m => m.id === id);
    if (!menu) return;

    elements.modalTitle.textContent = '✏️ 编辑菜单';
    elements.submitBtn.textContent = '💾 更新菜单';
    elements.editMenuId.value = id;
    elements.menuName.value = menu.name;
    elements.menuDesc.value = menu.desc || '';
    elements.menuTags.value = menu.tags.join(', ');
    elements.menuIngredients.value = menu.ingredients.join('\n');
    elements.menuSteps.value = menu.steps.join('\n');
    elements.uploadModal.classList.add('active');
}

function closeUploadModal() {
    elements.uploadModal.classList.remove('active');
}

function showTokenModal() {
    if (GITHUB_CONFIG.token) {
        showToast('🔒 Token 已内置配置');
        return;
    }
    elements.githubToken.value = state.githubToken;
    elements.tokenModal.classList.add('active');
}

function closeTokenModal() {
    elements.tokenModal.classList.remove('active');
}

function saveToken() {
    const token = elements.githubToken.value.trim();
    if (token) {
        state.githubToken = token;
        localStorage.setItem('githubToken', token);
        closeTokenModal();
        showToast('🔑 Token 已保存');
        github.load();
    } else {
        showToast('⚠️ 请输入有效的 Token');
    }
}

// ==================== CRUD 操作 ====================
async function handleSubmit(e) {
    e.preventDefault();
    if (state.isLoading) return;

    const editId = elements.editMenuId.value;
    const name = elements.menuName.value.trim();
    const desc = elements.menuDesc.value.trim();

    const menuData = {
        name,
        desc,
        tags: utils.parseTags(elements.menuTags.value),
        ingredients: utils.parseList(elements.menuIngredients.value),
        steps: utils.parseList(elements.menuSteps.value)
    };

    if (editId) {
        const index = state.menus.findIndex(m => m.id === parseInt(editId));
        if (index === -1) return;

        state.menus[index] = { ...state.menus[index], ...menuData };
        if (await github.save(`编辑菜单: ${name}`)) {
            renderMenus();
            closeUploadModal();
            showToast('💾 菜单更新成功！');
        }
    } else {
        const newMenu = {
            id: Date.now(),
            ...menuData,
            icon: utils.getRandomIcon()
        };
        state.menus.unshift(newMenu);
        if (await github.save(`新增菜单: ${name}`)) {
            renderMenus();
            closeUploadModal();
            showToast('✅ 菜单上传成功！');
        }
    }
}

async function deleteMenu(id, fromDetail = false) {
    const menu = state.menus.find(m => m.id === id);
    if (!menu || !confirm(`确定要删除「${menu.name}」吗？`)) return;

    state.menus = state.menus.filter(m => m.id !== id);
    if (await github.save(`删除菜单: ${menu.name}`)) {
        renderMenus();
        showToast('🗑️ 菜单已删除');
        if (fromDetail) backToHome();
    }
}

// ==================== 初始化 ====================
function init() {
    cacheElements();

    // 事件监听
    document.getElementById('uploadForm').addEventListener('submit', handleSubmit);
    elements.searchInput.addEventListener('input', utils.debounce(searchMenus, 300));
    elements.searchInput.addEventListener('keypress', e => { if (e.key === 'Enter') searchMenus(); });

    // 模态框外部点击关闭
    elements.uploadModal.addEventListener('click', e => { if (e.target === elements.uploadModal) closeUploadModal(); });
    elements.tokenModal.addEventListener('click', e => { if (e.target === elements.tokenModal) closeTokenModal(); });

    // 初始化图片上传
    initImageUpload();

    // 应用视图设置
    elements.gridViewBtn.classList.toggle('active', state.currentView === 'grid');
    elements.listViewBtn.classList.toggle('active', state.currentView === 'list');

    // 更新 Token 按钮状态
    if (GITHUB_CONFIG.token && elements.tokenBtn) {
        elements.tokenBtn.innerHTML = '🔒 Token 已配置';
        elements.tokenBtn.style.opacity = '0.7';
    }

    // 加载数据
    github.load().then(() => renderMenus());

    // 页面卸载时清理 Tesseract worker
    window.addEventListener('beforeunload', async () => {
        if (tesseractWorker) {
            await tesseractWorker.terminate();
        }
    });
}

// ==================== 图片上传与 OCR ====================
let currentImageFile = null;

function initImageUpload() {
    const uploadArea = document.getElementById('imageUploadArea');
    const fileInput = document.getElementById('dishImage');

    // 文件选择
    fileInput.addEventListener('change', handleFileSelect);

    // 拖拽上传
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) handleFile(file);
}

function handleFile(file) {
    if (!file.type.startsWith('image/')) {
        showToast('⚠️ 请选择图片文件');
        return;
    }

    currentImageFile = file;
    const reader = new FileReader();
    reader.onload = (e) => {
        document.getElementById('previewImg').src = e.target.result;
        // 使用 querySelector 获取 class
        const placeholder = document.querySelector('#imageUploadArea .upload-placeholder');
        if (placeholder) placeholder.style.display = 'none';
        document.getElementById('imagePreview').style.display = 'inline-block';
        document.getElementById('ocrButtons').style.display = 'flex';
    };
    reader.readAsDataURL(file);
}

function removeImage() {
    currentImageFile = null;
    document.getElementById('dishImage').value = '';
    document.getElementById('previewImg').src = '';
    const placeholder = document.querySelector('#imageUploadArea .upload-placeholder');
    if (placeholder) placeholder.style.display = 'block';
    document.getElementById('imagePreview').style.display = 'none';
    document.getElementById('ocrButtons').style.display = 'none';
    document.getElementById('ocrStatus').textContent = '';
}

// Tesseract Worker 实例
let tesseractWorker = null;

async function initTesseract() {
    if (tesseractWorker) return;

    try {
        // 创建 worker 并加载中文训练数据
        tesseractWorker = await Tesseract.createWorker('chi_sim', 1, {
            logger: message => {
                console.log('Tesseract:', message);
                const statusEl = document.getElementById('ocrStatus');
                if (statusEl && message.status) {
                    if (message.status === 'loading language traineddata') {
                        statusEl.textContent = '⏳ 正在加载中文语言包...';
                    } else if (message.status === 'recognizing text') {
                        statusEl.textContent = `🔍 识别中... ${Math.round(message.progress * 100)}%`;
                    }
                }
            },
            errorHandler: err => console.error('Tesseract Error:', err)
        });
    } catch (error) {
        console.error('初始化 Tesseract 失败:', error);
        throw error;
    }
}

async function recognizeImage() {
    if (!currentImageFile) {
        showToast('⚠️ 请先上传图片');
        return;
    }

    const statusEl = document.getElementById('ocrStatus');
    const btn = document.getElementById('recognizeBtn');

    statusEl.textContent = '⏳ 初始化识别引擎...';
    statusEl.classList.add('loading');
    btn.disabled = true;

    try {
        // 确保 worker 已初始化
        if (!tesseractWorker) {
            await initTesseract();
        }

        // 压缩图片以提高识别速度和准确率
        const compressedImage = await compressImage(currentImageFile, 1200);

        // 进行 OCR 识别
        const result = await tesseractWorker.recognize(compressedImage);
        const text = result.data.text;
        console.log('OCR 识别结果:', text);

        if (!text || text.trim().length === 0) {
            throw new Error('未能识别到文字');
        }

        // 解析识别结果并填充表单
        parseAndFillForm(text);

        statusEl.textContent = '✅ 识别完成';
        showToast('✅ 图片识别完成，已自动填充表单');
    } catch (error) {
        console.error('OCR 识别失败:', error);
        statusEl.textContent = '❌ 识别失败';

        // 显示具体错误信息
        let errorMsg = '图片识别失败';
        if (error.message && error.message.includes('network')) {
            errorMsg = '网络错误：无法下载语言包，请检查网络';
        } else if (error.message && error.message.includes('language')) {
            errorMsg = '语言包错误：中文训练数据加载失败';
        } else if (error.message && error.message.includes('createWorker')) {
            errorMsg = '引擎初始化失败，可能是浏览器兼容性问题';
        } else if (error.message) {
            errorMsg = error.message;
        }

        // 提供降级方案提示
        showToast(`❌ ${errorMsg}`);

        // 显示手动输入建议
        setTimeout(() => {
            if (confirm('AI 识别失败。是否尝试使用模拟识别（演示用）？\n\n或者您可以手动输入菜单信息。')) {
                simulateRecognition();
            }
        }, 500);
    } finally {
        statusEl.classList.remove('loading');
        btn.disabled = false;
    }
}

// 模拟识别（演示用，当真实 OCR 失败时提供）
function simulateRecognition() {
    const statusEl = document.getElementById('ocrStatus');
    statusEl.textContent = '🔍 模拟识别中...';

    // 模拟延迟
    setTimeout(() => {
        // 基于文件名的模拟数据
        const fileName = currentImageFile.name.toLowerCase();
        let mockData = {
            name: '识别示例菜',
            desc: '这是一道美味的家常菜',
            ingredients: ['主要食材 适量', '辅助食材 适量', '调味料 少许'],
            steps: ['1. 准备好所有食材', '2. 按照菜谱进行烹饪', '3. 调味后装盘即可'],
            tags: ['家常菜', '示例']
        };

        // 根据文件名猜测菜品类型
        if (fileName.includes('鸡') || fileName.includes('chicken')) {
            mockData = {
                name: '宫保鸡丁',
                desc: '经典川菜，麻辣鲜香',
                ingredients: ['鸡胸肉 300克', '花生米 50克', '干辣椒 10个', '花椒 1勺', '葱姜蒜 适量'],
                steps: ['1. 鸡肉切丁，用料酒、生抽腌制15分钟', '2. 花生米炸至金黄备用', '3. 热锅凉油，爆香花椒辣椒', '4. 下鸡丁炒至变色', '5. 加入调料汁和花生米翻炒均匀'],
                tags: ['川菜', '辣', '下饭菜']
            };
        } else if (fileName.includes('鱼') || fileName.includes('fish')) {
            mockData = {
                name: '清蒸鲈鱼',
                desc: '鲜美嫩滑，保留鱼肉原味',
                ingredients: ['鲈鱼 1条', '姜丝 适量', '葱丝 适量', '蒸鱼豉油 3勺'],
                steps: ['1. 鲈鱼处理干净，两面划几刀', '2. 铺上姜丝腌制10分钟', '3. 水开后蒸8-10分钟', '4. 淋上蒸鱼豉油即可'],
                tags: ['粤菜', '清淡', '海鲜']
            };
        } else if (fileName.includes('肉') || fileName.includes('pork') || fileName.includes('beef')) {
            mockData = {
                name: '红烧肉',
                desc: '肥而不腻，入口即化',
                ingredients: ['五花肉 500克', '冰糖 30克', '生抽 2勺', '老抽 1勺', '料酒 2勺'],
                steps: ['1. 五花肉切块，冷水下锅焯水', '2. 锅中放油，小火炒糖色', '3. 放入肉块翻炒上色', '4. 加入调料和适量水', '5. 小火炖煮45分钟至软烂'],
                tags: ['家常菜', '下饭菜', '经典']
            };
        }

        // 填充表单
        document.getElementById('menuName').value = mockData.name;
        document.getElementById('menuDesc').value = mockData.desc;
        document.getElementById('menuIngredients').value = mockData.ingredients.join('\n');
        document.getElementById('menuSteps').value = mockData.steps.join('\n');
        document.getElementById('menuTags').value = mockData.tags.join(', ');

        statusEl.textContent = '✅ 模拟识别完成（演示）';
        showToast('✅ 已使用演示数据填充表单，请根据实际情况修改');
    }, 1000);
}

// 图片压缩函数
function compressImage(file, maxWidth = 1200) {
    return new Promise((resolve, reject) => {
        const img = new Image();
        const reader = new FileReader();

        reader.onload = (e) => {
            img.src = e.target.result;
        };

        img.onload = () => {
            const canvas = document.createElement('canvas');
            let width = img.width;
            let height = img.height;

            // 等比例缩放
            if (width > maxWidth) {
                height = Math.round(height * maxWidth / width);
                width = maxWidth;
            }

            canvas.width = width;
            canvas.height = height;

            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0, width, height);

            // 转换为 base64
            const dataUrl = canvas.toDataURL('image/jpeg', 0.9);
            resolve(dataUrl);
        };

        img.onerror = reject;
        reader.readAsDataURL(file);
    });
}

function parseAndFillForm(text) {
    // 简单的文本解析逻辑
    const lines = text.split('\n').map(l => l.trim()).filter(l => l.length > 0);

    // 尝试提取菜名（通常是第一行或包含"菜名"、"名称"的行）
    let name = '';
    for (const line of lines) {
        if (line.includes('菜名') || line.includes('名称')) {
            name = line.replace(/菜名[：:]?/g, '').replace(/名称[：:]?/g, '').trim();
            break;
        }
    }
    if (!name && lines.length > 0) {
        name = lines[0].substring(0, 20); // 取第一行前20字符
    }
    if (name) document.getElementById('menuName').value = name;

    // 尝试提取食材（查找包含"食材"、"用料"、"材料"的区域）
    let ingredients = [];
    let inIngredientsSection = false;
    for (const line of lines) {
        if (line.includes('食材') || line.includes('用料') || line.includes('材料') || line.includes('原料')) {
            inIngredientsSection = true;
            continue;
        }
        if (inIngredientsSection && line.length > 1 && !line.includes('步骤') && !line.includes('做法')) {
            // 过滤掉可能的用量单位行
            if (/[克g毫升ml勺个根片]+/.test(line) || line.length < 30) {
                ingredients.push(line);
            }
        }
        if (line.includes('步骤') || line.includes('做法') || line.includes('制作')) {
            inIngredientsSection = false;
        }
    }
    if (ingredients.length > 0) {
        document.getElementById('menuIngredients').value = ingredients.join('\n');
    }

    // 尝试提取步骤（查找包含"步骤"、"做法"、"制作"的区域）
    let steps = [];
    let inStepsSection = false;
    let stepNum = 1;
    for (const line of lines) {
        if (line.includes('步骤') || line.includes('做法') || line.includes('制作') || line.includes('烹调')) {
            inStepsSection = true;
            continue;
        }
        if (inStepsSection && line.length > 5) {
            // 去除开头的数字序号
            const cleanLine = line.replace(/^\d+[.、.\s)）]+/, '').trim();
            if (cleanLine) {
                steps.push(`${stepNum}. ${cleanLine}`);
                stepNum++;
            }
        }
    }
    if (steps.length > 0) {
        document.getElementById('menuSteps').value = steps.join('\n');
    }

    // 尝试提取描述（如果没有食材和步骤的区域，可能整段都是描述）
    if (!ingredients.length && !steps.length && lines.length > 1) {
        const desc = lines.slice(1, 3).join('，');
        document.getElementById('menuDesc').value = desc;
    }

    // 智能标签推荐
    const tagMap = {
        '辣': ['川菜', '辣'],
        '麻辣': ['川菜', '辣'],
        '红烧': ['家常菜', '下饭菜'],
        '糖醋': ['家常菜', '甜酸'],
        '蒸': ['清淡', '健康'],
        '凉拌': ['快手菜', '素食'],
        '炒': ['快手菜', '家常菜'],
        '炖': ['家常菜', '汤'],
        '炸': ['小吃', '香脆'],
        '烤': ['西餐', '烤箱菜']
    };

    const suggestedTags = [];
    for (const [keyword, tags] of Object.entries(tagMap)) {
        if (text.includes(keyword)) {
            suggestedTags.push(...tags);
        }
    }
    if (suggestedTags.length > 0) {
        document.getElementById('menuTags').value = [...new Set(suggestedTags)].join(', ');
    }
}

// 启动
document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', init) : init();
