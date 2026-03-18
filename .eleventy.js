
module.exports = function(eleventyConfig) {
    // Pass through normal files
    eleventyConfig.addPassthroughCopy("src/assets");
    
    return {
        dir: {
            input: "src",
            output: "_site",
            includes: "_includes"
        }
    };
};
