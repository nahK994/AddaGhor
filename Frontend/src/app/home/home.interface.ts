interface Author {
  profilePic: string,
  name: string,
  userId: number
}

export interface Post {
  postId: number,
  text: string,
  author: Author,
  visibility: string
}

export interface Comment {
  commentId: number,
  author: Author,
  text: string,
}

export interface React {
  smile: number,
  love: number,
  like: number
}

export interface Reply {
  referenceId: number,
  text: string,
  author: Author
}

export interface ActivityFeed {
  post: Post,
  comments: Comment[],
  react: React,
  replies: Reply[]
}

// export interface PostComment {
//   commentId: number,
//   userId: number,
//   userName: string,
//   commentText: string,
//   commentDateTime: string,
//   avatar: string
// }