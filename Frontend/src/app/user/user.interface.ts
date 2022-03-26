export interface CreateUser
{
  userName: string,
  bio?: string,
  email: string,
  password: string,
  occupation: string
}

export interface User
{
  userId: number,
  userName: string,
  bio?: string,
  email: string,
  password: string,
  occupation: string
}

export interface LoginCredentialModel
{
  email: string,
  password: string
}