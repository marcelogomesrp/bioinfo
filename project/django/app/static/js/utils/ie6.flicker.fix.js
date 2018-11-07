//tenta eliminar o flicker bug
try {
    document.execCommand("BackgroundImageCache", false, true);
} catch(err) {}
