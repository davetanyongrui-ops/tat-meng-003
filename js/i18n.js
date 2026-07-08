(function() {
  // We wait for the DOM to be fully loaded
  document.addEventListener('DOMContentLoaded', () => {
    initTranslations();
    
    // Check local storage for language
    const savedLang = localStorage.getItem('site_lang') || 'en';
    if (savedLang !== 'en') {
      applyTranslations(savedLang);
    }
  });

  function initTranslations() {
    // Traverse the DOM and save original text on the nodes themselves
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    let node;
    while(node = walker.nextNode()) {
      const text = node.nodeValue;
      if(text && text.trim().length > 0) {
        node._originalText = text;
      }
    }
    
    // Also save placeholders for inputs/textareas
    document.querySelectorAll('[placeholder]').forEach(el => {
      if (!el._originalPlaceholder) {
        el._originalPlaceholder = el.getAttribute('placeholder');
      }
    });
  }

  function applyTranslations(lang) {
    if (!window.siteTranslations) return;
    
    const dict = window.siteTranslations;
    
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    let node;
    while(node = walker.nextNode()) {
      if(node._originalText) {
        const trimmed = node._originalText.trim();
        if (dict[trimmed]) {
          const translation = lang === 'en' ? trimmed : (dict[trimmed][lang] || trimmed);
          // Preserve leading/trailing whitespace
          const newText = node._originalText.replace(trimmed, translation);
          if (node.nodeValue !== newText) {
            node.nodeValue = newText;
          }
        }
      }
    }
    
    // Update placeholders
    document.querySelectorAll('[placeholder]').forEach(el => {
      if (el._originalPlaceholder) {
        const trimmed = el._originalPlaceholder.trim();
        if (dict[trimmed]) {
          const translation = lang === 'en' ? trimmed : (dict[trimmed][lang] || trimmed);
          el.setAttribute('placeholder', translation);
        }
      }
    });
    
    // Update the language switcher button text
    const btn = document.getElementById('langSwitcherBtn');
    if (btn) {
      const langLabels = {
        'en': 'EN',
        'zh': 'ZH',
        'id': 'ID'
      };
      
      const svgIcon = '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"></path></svg>';
      btn.innerHTML = svgIcon + ' ' + (langLabels[lang] || 'EN');
      
      // Update original text on the new text node created by innerHTML, so it doesn't get overwritten incorrectly next time
      const btnWalker = document.createTreeWalker(btn, NodeFilter.SHOW_TEXT, null, false);
      let btnNode;
      while (btnNode = btnWalker.nextNode()) {
          btnNode._originalText = btnNode.nodeValue;
      }
    }
  }

  // Global function for the language switcher UI to call
  window.switchLanguage = function(lang) {
    localStorage.setItem('site_lang', lang);
    applyTranslations(lang);
    
    // Dispatch an event just in case other scripts want to react
    window.dispatchEvent(new CustomEvent('languageChanged', { detail: { lang } }));
  };
})();
