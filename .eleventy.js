
module.exports = function(eleventyConfig) {
    // Pass through normal files
    eleventyConfig.addPassthroughCopy("src/assets");
    
    // Add date filter
    eleventyConfig.addFilter("date", (dateObj, format) => {
        const d = dateObj instanceof Date ? dateObj : new Date(dateObj);
        return d.toLocaleDateString('en-US', {
            month: 'long',
            day: 'numeric',
            year: 'numeric'
        });
    });
    
    return {
        dir: {
            input: "src",
            output: "_site",
            includes: "_includes"
        }
    };
};
