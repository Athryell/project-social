const posts = document.querySelectorAll('.edit-post')
const likeButtons = document.querySelectorAll('.like-icon')
const unLikeButtons = document.querySelectorAll('.unlike-icon')
const likeCount = document.querySelectorAll('.like-count')
const userId = JSON.parse(document.getElementById('user_id').textContent)

let post_ids = JSON.parse(localStorage.getItem('post_liked'))

if (!localStorage.getItem('post_liked')) {
    // If not, set the counter to empty array in local storage
    localStorage.setItem('post_liked', JSON.stringify([]));
}

likeCount.forEach(btn => {
    btn.textContent = btn.dataset.likes
})

likeButtons.forEach(btn => {
    const post_id = btn.dataset.id
    if (post_ids.includes(post_id)){
        btn.hidden = true
    }
})

unLikeButtons.forEach(btn => {
    const post_id = btn.dataset.id
    if (post_ids.includes(post_id)){
        btn.hidden = false
    }
})


likeButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        const post_id = btn.dataset.id

        increase_likes(post_id, btn)
        .catch(err => console.error(err))

        /* Adding to local variable */
        post_ids.push(post_id)
        localStorage.setItem('post_liked', JSON.stringify(post_ids))

        btn.hidden = true
        btn.nextElementSibling.hidden = false
    })
})

unLikeButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        const post_id = btn.dataset.id

        decrease_likes(post_id, btn)
        .catch(err => console.error(err))

        /* Removing from local variable */
        const index = post_ids.indexOf(post_id)
            if (index > -1) {
            post_ids.splice(index, 1);
            }
        localStorage.setItem('post_liked', JSON.stringify(post_ids))

        btn.hidden = true
        btn.previousElementSibling.hidden = false
    })
})

async function increase_likes(post_id, btn){
    /* Get the number of likes from the post */
    const response = await fetch(`/posts/${post_id}`)
    const post = await response.json()
    const new_like_count = post.likes + 1

    /* Add one like and update the post info */
    const settings = {
        method: 'PUT',
        body: JSON.stringify({
            likes: new_like_count,
        })
    }
    await fetch(`/posts/${post_id}`, settings)
    
    /* Just don't mess with the html... */
    btn.nextElementSibling.nextElementSibling.textContent = new_like_count
}

async function decrease_likes(post_id, btn){
    /* Get the number of likes from the post */
    const response = await fetch(`/posts/${post_id}`)
    const post = await response.json()
    const new_like_count = post.likes - 1

    /* Add one like and update the post info */
    const settings = {
        method: 'PUT',
        body: JSON.stringify({
            likes: new_like_count
        })
    }
    await fetch(`/posts/${post_id}`, settings)

    /* Just don't mess with the html... */
    btn.nextElementSibling.textContent = new_like_count
}

posts.forEach(post => {
    post.addEventListener('click', () => {
        /* Get the element from the same html article */
        const article_content = post.parentElement.previousElementSibling
        const save_btn = post.nextElementSibling
        const p_to_replace = article_content.querySelector('p')

        /* Replace text with editable textarea */
        const edit_area = document.createElement('textarea')
        edit_area.textContent = article_content.textContent.trim()
        article_content.replaceChild(edit_area, p_to_replace)

        /* Swap buttons edit <-> save */
        post.hidden = true
        save_btn.hidden = false

        save_btn.addEventListener('click', saveEditText)
    })
}) 

function saveEditText(e){
    const save_btn = e.target
    const article_content = save_btn.parentElement.previousElementSibling
    const edit_icon = save_btn.previousElementSibling
    const textarea_to_replace = article_content.querySelector('textarea')

    /* Save edited text */
    const new_content = document.createElement('p')
    text = textarea_to_replace.value.trim()
    post_id = save_btn.dataset.id

    new_content.textContent = text
    article_content.replaceChild(new_content, textarea_to_replace)

    change_text(post_id, text)

    /* Swap buttons edit <-> save */
    edit_icon.hidden = false
    save_btn.hidden = true
}

function change_text(post_id, text){
    fetch(`/posts/${post_id}`, {
      method: 'PUT',
      body: JSON.stringify({
        content: text
      })
    })
  }

