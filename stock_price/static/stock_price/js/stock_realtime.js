const StockApp = {
    stockList: [], // 자동완성용 종목 리스트
    version: "1.2", // For cache verification
    socket: null,
    stockCode: null,


    init: function () {
        console.log(`StockApp Initialized (Version ${this.version})`);
        this.cacheDOM();
        // ... (existing code) ...
        this.bindEvents();

        // Initialize Autocomplete
        this.autocomplete = new StockAutocomplete({
            inputId: 'stock-code-input',
            shortCodeInputId: 'selected-short-code',
            onSelect: (item) => {
                // When item selected, connect immediately
                this.connectWS();
            },
            onReady: () => {
                // 1. Check URL params after list is loaded
                const urlParams = new URLSearchParams(window.location.search);
                const codeParam = urlParams.get('code');
                const nameParam = urlParams.get('name');

                if (codeParam && nameParam) {
                    this.$input.value = nameParam;
                    if (this.$selectedShortCode) this.$selectedShortCode.value = codeParam;
                    // Connect immediately if params are present
                    this.connectWS();
                }
            }
        });
    },

    cacheDOM: function () {
        this.$input = document.getElementById('stock-code-input');
        this.$selectedShortCode = document.getElementById('selected-short-code');
        this.$connectBtn = document.getElementById('connect-btn');
        this.$disconnectBtn = document.getElementById('disconnect-btn');
        this.$detailBtn = document.getElementById('detail-btn');
        this.$status = document.getElementById('status');
        this.$askTable = document.getElementById('ask-table-body');
        this.$bidTable = document.getElementById('bid-table-body');
        this.$currentPrice = document.getElementById('current-price');
        this.$currentPriceDiff = document.getElementById('current-price-diff');
    },

    bindEvents: function () {
        this.$connectBtn.addEventListener('click', () => this.connectWS());
        this.$disconnectBtn.addEventListener('click', () => this.disconnectWS());
        if (this.$detailBtn) {
            this.$detailBtn.addEventListener('click', () => this.goToDetail());
        }

        // 엔터키 입력 시 연결
        this.$input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.connectWS();
            }
        });
    },

    goToDetail: function () {
        // 1. If currently connected, use that code
        let code = this.stockCode;

        // 2. If not connected, or input changed, try to resolve from input
        if (!code) {
            const inputVal = this.$input.value.trim();
            if (this.$selectedShortCode && this.$selectedShortCode.value) {
                code = this.$selectedShortCode.value;
            } else if (inputVal) {
                // Try to find by name
                const match = this.autocomplete.findStock(inputVal);
                if (match) {
                    code = match.short_code;
                } else if (/^\d{6}$/.test(inputVal)) {
                    // Assume input is code
                    code = inputVal;
                }
            }
        }

        if (code) {
            window.location.href = `/stock_price/stock/detail/${code}/`;
        } else {
            alert('먼저 종목을 조회하거나 올바른 종목명을 입력해주세요.');
        }
    },

    disconnectWS: function () {
        if (this.socket) {
            console.log("Disconnecting current socket...");
            this.socket.close();
            this.socket = null;
            this.updateStatus('연결 종료됨');
        }
    },

    connectWS: function () {
        // prefer selected short code (from autocomplete). If absent, use raw input.
        let code = (this.$selectedShortCode && this.$selectedShortCode.value) ? this.$selectedShortCode.value : this.$input.value.trim();

        // If code is not a valid 6-digit code, try to resolve it as a name
        let stockName = '';

        // Try to find the stock object to get the clean name
        const match = this.autocomplete.findStock(code);
        if (match) {
            code = match.short_code;
            stockName = match.name;
            // Update inputs to match selection
            this.$input.value = stockName;
            if (this.$selectedShortCode) this.$selectedShortCode.value = code;
        } else if (/^\d{6}$/.test(code)) {
            // If it was a raw code, try to look up the name for the URL
            // (match is null, but maybe we can find it now that we know it's a code)
            const paramMatch = this.autocomplete.findStock(code);
            if (paramMatch) {
                stockName = paramMatch.name;
                // Only update input value if it's currently showing the code or empty, to avoid overwriting user edits?
                // Actually, if we resolved a name, we should show it.
                this.$input.value = stockName;
            } else {
                stockName = code; // Fallback
            }
        } else {
            // Valid name logic handled above, this else is for "not code AND not found"
            console.warn("Could not resolve stock name:", code);
        }

        if (!code) {
            alert('종목코드를 입력해주세요.');
            return;
        }

        // Update URL to reflect current stock
        try {
            if (history.pushState) {
                const newUrl = `${window.location.pathname}?code=${code}&name=${encodeURIComponent(stockName)}`;
                console.log(`Updating URL to: ${newUrl}`);
                window.history.pushState({ path: newUrl }, '', newUrl);
            }
        } catch (e) {
            console.error("Failed to update URL", e);
        }

        console.log(`Attempting to connect to stock: ${code}`);

        // UI 초기화 및 호가 테이블 구조 미리 생성
        this.initHogaTables();
        this.$currentPrice.textContent = '-';
        this.$currentPriceDiff.textContent = '-';
        this.$currentPrice.className = 'current-price-value';
        this.$currentPriceDiff.className = 'diff';

        this.stockCode = code;
        this.disconnectWS();

        this.updateStatus('연결 시도 중...');
        this.socket = new WebSocket('ws://' + window.location.host + '/ws/stock/' + code + '/');

        this.socket.onopen = () => this.updateStatus(`연결됨 (${code})`);
        this.socket.onmessage = (event) => this.handleMessage(event);
        this.socket.onclose = () => this.updateStatus('연결 끊김');
        this.socket.onerror = (error) => {
            console.error('WebSocket Error:', error);
            this.updateStatus('에러 발생');
        };
    },

    initHogaTables: function () {
        // 매도 호가 테이블 초기화 (10행)
        let askHtml = '';
        for (let i = 10; i >= 1; i--) {
            askHtml += `
                <tr class="ask-row" data-index="${i}">
                    <td class="volume">-</td>
                    <td class="price">-</td>
                    <td class="rate"></td>
                </tr>
            `;
        }
        this.$askTable.innerHTML = askHtml;

        // 매수 호가 테이블 초기화 (10행)
        let bidHtml = '';
        for (let i = 1; i <= 10; i++) {
            if (i === 1) {
                // 첫 번째 행의 첫 번째 칸에 체결 리스트 영역(rowspan=10) 추가
                bidHtml += `
                    <tr class="bid-row" data-index="${i}">
                        <td rowspan="10" class="trade-area">
                            <div class="trade-list-wrap">
                                <table class="trade-list-table">
                                    <tbody id="trade-list">
                                        <!-- JS insert -->
                                    </tbody>
                                </table>
                            </div>
                        </td>
                        <td class="price">-</td>
                        <td class="volume">-</td>
                    </tr>
                `;
            } else {
                bidHtml += `
                    <tr class="bid-row" data-index="${i}">
                        <td class="price">-</td>
                        <td class="volume">-</td>
                    </tr>
                `;
            }
        }
        this.$bidTable.innerHTML = bidHtml;
    },

    updateStatus: function (msg) {
        this.$status.textContent = msg;
    },

    handleMessage: function (event) {
        try {
            const data = JSON.parse(event.data);

            // 1. 호가 데이터 (10호가가 모두 있어야 진짜 호가 데이터임)
            // 체결 데이터에도 ASKP1, BIDP1은 포함되어 있어서 오동작함 -> ASKP10, BIDP10 체크로 구분
            if (data.ASKP10 !== undefined && data.BIDP10 !== undefined) {
                this.renderHoga(data);
            }

            // 2. 체결 데이터
            if (data.STCK_PRPR !== undefined && data.STCK_CNTG_HOUR) {
                this.renderExecution(data);
            }
        } catch (e) {
            console.error("Parse Error", e);
        }
    },

    renderExecution: function (data) {
        const price = data.STCK_PRPR;
        const diff = data.PRDY_VRSS;
        const rate = data.PRDY_CTRT;
        const vol = data.CNTG_VOL;

        // 1 (Buy/Ask) -> Red/Up, 5 (Sell/Bid) -> Blue/Down
        // If CCLD_DVSN is available, use it. Otherwise fallback to diff.
        let colorClass = '';
        if (data.CCLD_DVSN) {
            if (data.CCLD_DVSN === '1') colorClass = 'up'; // Buy (Ask) -> Red
            else if (data.CCLD_DVSN === '5') colorClass = 'down'; // Sell (Bid) -> Blue
        } else {
            // Fallback
            if (diff > 0) colorClass = 'up';
            else if (diff < 0) colorClass = 'down';
        }

        this.updateCurrentPrice(price, diff, rate, data.PRDY_VRSS_SIGN);

        // 체결 목록 추가 (최근 15개 유지)
        const $tradeList = document.getElementById('trade-list');
        if ($tradeList) {
            const row = document.createElement('tr');
            // Remove time, show Price and Volume
            // Price gets color
            row.innerHTML = `
                <td class="${colorClass}">${StockUtils.formatNumber(price)}</td>
                <td>${StockUtils.formatNumber(vol)}</td>
            `;
            $tradeList.prepend(row);
            if ($tradeList.children.length > 15) {
                $tradeList.lastElementChild.remove();
            }
        }
    },

    updateCurrentPrice: function (price, diff, rate, sign) {
        const formattedPrice = StockUtils.formatNumber(price);
        if (this.$currentPrice.textContent !== formattedPrice) {
            // 가격이 변했을 때만 업데이트 및 효과
            const prevPrice = parseInt(this.$currentPrice.textContent.replace(/,/g, '')) || 0;
            this.$currentPrice.textContent = formattedPrice;

            if (price > prevPrice) StockUtils.triggerFlash(this.$currentPrice, 'up');
            else if (price < prevPrice) StockUtils.triggerFlash(this.$currentPrice, 'down');
        }

        let diffSign = '';
        if (sign) {
            if (sign === '1' || sign === '2') diffSign = '▲';
            else if (sign === '4' || sign === '5') diffSign = '▼';
        } else {
            diffSign = diff > 0 ? '+' : '';
        }

        const diffText = `${diffSign}${StockUtils.formatNumber(Math.abs(diff))} (${rate}%)`;
        if (this.$currentPriceDiff.textContent !== diffText) {
            this.$currentPriceDiff.textContent = diffText;
        }

        // 색상 처리
        let colorClass = '';
        if (sign) {
            if (sign === '1' || sign === '2') colorClass = 'up';
            else if (sign === '4' || sign === '5') colorClass = 'down';
        } else {
            if (diff > 0) colorClass = 'up';
            else if (diff < 0) colorClass = 'down';
        }

        this.$currentPrice.className = `current-price-value ${colorClass}`;
        this.$currentPriceDiff.className = `diff ${colorClass}`;
    },

    // triggerFlash removed (using StockUtils)

    // formatNumber removed (using StockUtils)

    renderHoga: function (data) {
        // 매도 호가 업데이트
        for (let i = 1; i <= 10; i++) {
            this.updateHogaRow(this.$askTable, i, data[`ASKP${i}`], data[`ASKP_RSQN${i}`], 'ask');
        }

        // 매수 호가 업데이트
        for (let i = 1; i <= 10; i++) {
            this.updateHogaRow(this.$bidTable, i, data[`BIDP${i}`], data[`BIDP_RSQN${i}`], 'bid');
        }
    },

    updateHogaRow: function ($container, index, price, volume, type) {
        const row = $container.querySelector(`tr[data-index="${index}"]`);
        if (!row) return;

        const priceEl = row.querySelector('.price');
        const volumeEl = row.querySelector('.volume');

        const formattedPrice = StockUtils.formatNumber(price);
        const formattedVolume = StockUtils.formatNumber(volume);

        if (priceEl.textContent !== formattedPrice) {
            const prevPrice = parseInt(priceEl.textContent.replace(/,/g, '')) || 0;
            priceEl.textContent = formattedPrice;
            if (prevPrice !== 0) {
                StockUtils.triggerFlash(priceEl, price > prevPrice ? 'up' : 'down');
            }
        }

        if (volumeEl.textContent !== formattedVolume) {
            const prevVol = parseInt(volumeEl.textContent.replace(/,/g, '')) || 0;
            volumeEl.textContent = formattedVolume;
            if (prevVol !== 0) {
                StockUtils.triggerFlash(volumeEl, volume > prevVol ? 'up' : 'down');
            }
        }
    }
};

document.addEventListener('DOMContentLoaded', () => {
    StockApp.init();
});
