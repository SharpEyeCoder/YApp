// Feed.js

import React from 'react';
import Post from '../components/Post';

const Feed = ({ posts }) => {
    return (
        <div>
            <h1>Feed</h1>
            {posts.map(post => (
                <Post key={post.id} content={post.content} />
            ))}
        </div>
    );
};

export default Feed;