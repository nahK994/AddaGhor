export interface CreateUser
{
  userName: string,
  bio?: string,
  email: string,
  password: string,
  occupation: string,
  avatar: string
}

export interface User
{
  userId: number,
  userName: string,
  bio?: string,
  email: string,
  password: string,
  occupation: string,
  avatar: string
}
