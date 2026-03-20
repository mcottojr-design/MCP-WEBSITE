
module.exports = function(eleventyConfig) {
    // Pass through normal files
    eleventyConfig.addPassthroughCopy("src/assets");
    eleventyConfig.addPassthroughCopy("src/admin");
    
    // Add date filter - handles format strings used in templates
    eleventyConfig.addFilter("date", (dateObj, format) => {
        const d = dateObj instanceof Date ? dateObj : new Date(dateObj);
        if (format === 'MMM DD' || format === 'MMM D') {
            return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        }
        // Default: full date (covers MMMM D, YYYY and no-arg usage)
        return d.toLocaleDateString('en-US', {
            month: 'long',
            day: 'numeric',
            year: 'numeric'
        });
    });

    // Add limit filter
    eleventyConfig.addFilter("limit", (array, limit) => {
        return array.slice(0, limit);
    });
    
    return {
        dir: {
            input: "src",
            output: "_site",
            includes: "_includes"
        },
        htmlTemplateEngine: "njk",
        markdownTemplateEngine: "njk"
    };
};
