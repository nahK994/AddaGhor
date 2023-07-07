import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";


@Injectable()
export class AccessTokenInterceptor implements HttpInterceptor {

    constructor() { }

    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        let tokenizedRequest = request;
        const token = sessionStorage.getItem("JWT_TOKEN");
        if (token !== "undefined" && token !== null) {
            const tokenValue = 'Bearer ' + token;
            tokenizedRequest = request.clone({ setHeaders: { Authorization: tokenValue } });
        }
        return next.handle(tokenizedRequest);
    }
}